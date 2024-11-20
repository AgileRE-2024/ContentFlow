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
            for h in headings:
                h_length = len(h.get_text())
                if 20 <= h_length <= 70:
                    criteria_scores['Heading Length'] += 10
                elif 15 <= h_length < 20:
                    criteria_scores['Heading Length'] += 5

            # Skor 4: Keyword di judul
            keyword_in_title_count = sum(title.lower().count(keyword.lower()) for keyword, _ in keywords)
            if keyword_in_title_count == 1:
                criteria_scores['Keyword in Title'] = 10
            elif keyword_in_title_count == 2:
                criteria_scores['Keyword in Title'] = 5
            else:
                criteria_scores['Keyword in Title'] = 0

            # Skor 5: Keyword di paragraf pertama
            if first_paragraph:
                keyword_in_first_paragraph_count = sum(first_paragraph.lower().count(keyword.lower()) for keyword, _ in keywords)
                if keyword_in_first_paragraph_count in [1, 2]:
                    criteria_scores['Keyword in First Paragraph'] = 10
                elif keyword_in_first_paragraph_count == 3:
                    criteria_scores['Keyword in First Paragraph'] = 5
                else:
                    criteria_scores['Keyword in First Paragraph'] = 0
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

            # Data untuk template
            result_data = {
                'url': url,
                'title': title,
                'content': content,
                'total_score': total_score,
                'criteria_scores': criteria_scores,
                'keywords': [keyword for keyword, _ in keywords]
            }

            return render(request, 'analysis-result.html', {'result': result_data})

        except requests.exceptions.RequestException as e:
            return render(request, 'analysis-url.html', {'error': f'Gagal mengambil data: {e}'})

    return render(request, 'analysis-url.html', {'error': 'Hanya metode POST yang diperbolehkan.'})