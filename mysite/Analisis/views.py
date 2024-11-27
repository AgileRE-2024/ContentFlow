from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import Counter
import re
from urllib.parse import urlparse

# Landing Page
def LandingPage(request):
    return render(request, 'landingpage.html')

# Halaman untuk menginput URL yang ingin dianalisis
def RecommendationURL(request):
    return render(request, 'recommendation-url.html')

# Halaman input untuk analisis URL
def AnalysisURL(request):
    return render(request, 'analysis-url.html')

# Hasil Analisis URL
def AnalysisResult(request):
    if request.method == 'POST':
        url = request.POST.get('url')  # Ambil URL dari input form

        if not url:
            return render(request, 'analysis-url.html', {'error': 'URL tidak boleh kosong.'})

        try:
            # Ambil konten dari URL
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text

            # Parsing HTML menggunakan BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Ambil judul artikel
            title = soup.title.string if soup.title else 'No Title Found'
            title_length = len(title)

            # Ambil konten dari elemen <body>
            body_content = soup.find('body')
            content = body_content.get_text(separator='\n', strip=True) if body_content else 'No body content found.'

            # Ambil semua heading
            headings = soup.find_all(['h1', 'h2', 'h3'])
            heading_count = len(headings)

            # Ambil meta description
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_content = meta_description['content'] if meta_description else ''
            meta_length = len(meta_content)

            # Ambil gambar dan alt text
            images = soup.find_all('img')
            alt_count = sum(1 for img in images if img.get('alt'))

            # Ambil paragraf pertama
            all_paragraphs = soup.find_all('p')
            first_paragraph = all_paragraphs[0].get_text(strip=True) if all_paragraphs else None

            # Kata kunci yang ingin dicari
            keyword = "keyword utama"  # Ganti sesuai kebutuhan
            keyword_found = []
            if keyword.lower() in content.lower():
                keyword_found.append(keyword)

            # Cari kata kunci teratas
            stop_words = set(stopwords.words('indonesian') + stopwords.words('english'))
            words = re.findall(r'\b\w+\b', content.lower())
            filtered_words = [word for word in words if word not in stop_words]
            word_counts = Counter(filtered_words)
            keywords = word_counts.most_common(3)

            # Ambil domain dari URL
            page_domain = urlparse(url).netloc

            # Cari tautan internal dan eksternal
            internal_links = []
            external_links = []
            for link in soup.find_all('a', href=True):
                parsed_link = urlparse(link['href'])
                if not parsed_link.netloc or parsed_link.netloc == page_domain:
                    internal_links.append(link['href'])
                else:
                    external_links.append(link['href'])

            # Skoring berdasarkan kriteria SEO
            criteria_scores = {}

            # Skor 1: Panjang judul
            if 50 <= title_length <= 60:
                criteria_scores['Title Length'] = 10
            elif 45 <= title_length < 50 or 60 < title_length <= 65:
                criteria_scores['Title Length'] = 5
            else:
                criteria_scores['Title Length'] = 0

            # Skor 2: Jumlah heading
            if 2 <= heading_count <= 3:
                criteria_scores['Heading Count'] = 10
            elif heading_count == 1:
                criteria_scores['Heading Count'] = 5
            else:
                criteria_scores['Heading Count'] = 0

            # Skor 3: Panjang heading
            criteria_scores['Heading Length'] = 0

            if headings:  # Periksa apakah ada heading
                optimal_count = 0
                total_headings = len(headings)
    
                for h in headings:
                    h_length = len(h.get_text().strip())
                    if 20 <= h_length <= 70:
                        optimal_count += 1
    
                # Penilaian berdasarkan jumlah heading yang optimal
                if optimal_count == total_headings:  # Semua heading optimal
                    criteria_scores['Heading Length'] = 10
                elif optimal_count > 0:  # Beberapa heading optimal
                    criteria_scores['Heading Length'] = 5
                else:  # Tidak ada heading optimal
                    criteria_scores['Heading Length'] = 0
            else:
                criteria_scores['Heading Length'] = 0  # Tidak ada heading sama sekali


            # Skor 4: Keyword di judul
            keyword_in_title_count = sum(title.lower().count(keyword.lower()) for keyword, _ in keywords)
            if keyword_in_title_count == 1:
                criteria_scores['Keyword in Title'] = 10
            elif keyword_in_title_count == 2:
                criteria_scores['Keyword in Title'] = 5
            else:
                criteria_scores['Keyword in Title'] = 0

            # Skor 5: Keyword di paragraf pertama
            keyword_in_first_paragraph_count = sum(first_paragraph.lower().count(keyword.lower()) for keyword, _ in keywords)
            if keyword_in_first_paragraph_count in [1, 2]:
                criteria_scores['Keyword in First Paragraph'] = 10
            elif keyword_in_first_paragraph_count == 3:
                criteria_scores['Keyword in First Paragraph'] = 5
            else:
                criteria_scores['Keyword in First Paragraph'] = 0

            # Skor 6: Panjang konten
            word_count = len(content.split())
            if 300 <= word_count <= 1500:
                criteria_scores['Content Length'] = 10
            else:
                criteria_scores['Content Length'] = 0

            # Skor 7: Alt tag pada gambar
            if len(images) == 0:
                criteria_scores['Alt Tag on Images'] = 0
            elif alt_count == len(images):
                criteria_scores['Alt Tag on Images'] = 10
            elif alt_count > 0:
                criteria_scores['Alt Tag on Images'] = 5
            else:
                criteria_scores['Alt Tag on Images'] = 0

            # Skor 8: Meta tag
            if 0 <= meta_length <= 160 and keyword in meta_content:
                criteria_scores['Meta Tag'] = 10
            elif 0 <= meta_length <= 160:
                criteria_scores['Meta Tag'] = 5
            else:
                criteria_scores['Meta Tag'] = 0

            # Skor 9: Internal link
            criteria_scores['Internal Links'] = 10 if internal_links else 0

            # Skor 10: External link
            criteria_scores['External Links'] = 10 if external_links else 0

            # Total skor
            total_score = sum(criteria_scores.values())
            
            # Rekomendasi perbaikan
            recommendations = {

                'Title Length': {
                    0: "Judul artikel Anda terlalu pendek. Perpanjang hingga mencapai panjang optimal antara 50-60 karakter untuk meningkatkan efektivitas SEO dan menarik perhatian pembaca.",
                    5: "Judul artikel Anda sudah cukup baik, namun jika memungkinkan, coba sesuaikan panjangnya agar berada di rentang optimal 50-60 karakter."
                },
                'Heading Count': {
                    0: "Artikel Anda membutuhkan lebih banyak heading (H1, H2, H3) untuk memberikan struktur yang jelas. Ini akan memudahkan pembaca memahami isi artikel dan meningkatkan nilai SEO.",
                    5: "Heading yang digunakan sudah cukup, tetapi menambah satu atau dua heading lagi dapat membuat struktur konten lebih informatif dan optimal."
                },
                'Heading Length': {
                    0: "Beberapa heading terlalu pendek atau terlalu panjang. Cobalah untuk menyesuaikan panjang heading agar berada di rentang optimal 20-70 karakter sehingga lebih relevan bagi pembaca dan mesin pencari.",
                    5: "Heading dalam artikel Anda sudah baik, tetapi ada yang dapat sedikit diperbaiki agar panjangnya lebih sesuai dengan rentang optimal 20-70 karakter."
                },
                'Keyword in Title': {
                    0: "Kata kunci utama belum muncul di judul artikel. Pastikan untuk menyisipkan kata kunci utama agar relevansi artikel dengan pencarian lebih tinggi.",
                    5: "Kata kunci utama sudah ada di judul, tetapi pertimbangkan untuk memperkuat posisinya atau menggunakannya secara lebih menonjol."
                },
                'Keyword in First Paragraph': {
                    0: "Kata kunci utama belum disebutkan di paragraf pertama. Tambahkan kata kunci utama di bagian awal untuk membantu mesin pencari mengenali topik artikel Anda.",
                    5: "Paragraf pertama sudah mengandung kata kunci utama, namun Anda bisa menyebutkannya sekali lagi untuk meningkatkan relevansi SEO."
                },
                'Content Length': {
                    0: "Panjang artikel masih kurang dari rekomendasi SEO. Tambahkan lebih banyak konten hingga mencapai panjang ideal (300-1500 kata) untuk memberikan nilai lebih bagi pembaca dan mesin pencari.",
                    5: "Artikel Anda hampir mencapai panjang optimal, tetapi menambahkan beberapa paragraf tambahan dapat memberikan dampak yang lebih signifikan untuk SEO."
                },
                'Alt Tag on Images': {
                    0: "Gambar di artikel belum memiliki tag 'alt'. Pastikan untuk menambahkan tag 'alt' yang relevan pada setiap gambar agar meningkatkan aksesibilitas dan SEO.",
                    5: "Sebagian besar gambar sudah memiliki tag 'alt', tetapi pastikan semua gambar lainnya juga dilengkapi dengan deskripsi yang relevan."
                },
                'Meta Tag': {
                    0: "Meta description pada artikel Anda belum dioptimalkan. Perbaiki atau tambahkan meta description yang mencakup kata kunci utama untuk meningkatkan relevansi artikel di search engine.",
                    5: "Meta description sudah mencakup kata kunci utama, namun pastikan deskripsinya menarik dan sesuai dengan isi artikel untuk hasil yang lebih baik."
                },
                'Internal Links': {
                    0: "Artikel Anda belum menyertakan tautan internal ke konten lain di situs. Tambahkan tautan internal untuk memudahkan navigasi pembaca dan meningkatkan SEO.",
                    5: "Internal links sudah ada, tetapi menambah tautan ke artikel lain yang relevan dapat meningkatkan nilai konten Anda di mata pembaca dan search engine."
                },
                'External Links': {
                    0: "Artikel Anda belum menyertakan tautan ke sumber eksternal. Tambahkan tautan ke sumber yang relevan untuk meningkatkan kredibilitas konten.",
                    5: "Tautan eksternal sudah digunakan, tetapi menambahkan tautan ke sumber berkualitas tinggi dapat memperkuat otoritas artikel Anda."
                }
            }

            # Menambahkan rekomendasi pada result_data
            recommendation_data = {
                key: recommendations[key].get(score, "-") 
                for key, score in criteria_scores.items()
            }

            # Data untuk template
            result_data = {
                'url': url,
                'title': title,
                'content': content,
                'total_score': total_score,
                'criteria_scores': criteria_scores,
                'recommendations': recommendation_data,
                'keywords': [keyword for keyword, _ in keywords]
            }

            return render(request, 'analysis-result.html', {'result': result_data})

        except requests.exceptions.RequestException as e:
            return render(request, 'analysis-url.html', {'error': f'Gagal mengambil data: {e}'})
    return render(request, 'analysis-url.html')

def FAQ(request):
    return render(request, 'faq.html')
