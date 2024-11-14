from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import Counter
import re

def LandingPage(request):
    return render(request, 'landingpage.html')

def RecommendationURL(request):
    return render(request, 'recommendation-url.html')

def AnalysisURL(request):
    return render(request, 'analysis-url.html')

def AnalysisResult(request):
    if request.method == 'POST':
        url = request.POST.get('url')  # Ambil URL dari input form

        try:
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')

            # Ambil judul artikel
            title = soup.title.string if soup.title else 'No Title Found'
            title_length = len(title)
            
            # Ambil konten dari elemen <body>
            body_content = soup.find('body')
            if body_content:
                content = body_content.get_text(separator='\n', strip=True)
            else:
                content = 'No body content found.'

            # Ambil heading
            headings = soup.find_all(['h1', 'h2', 'h3'])
            heading_count = len(headings)

            # Ambil meta description
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_content = meta_description['content'] if meta_description else ''
            meta_length = len(meta_content)

            # Ambil gambar dan alt text
            images = soup.find_all('img')
            alt_count = sum(1 for img in images if img.get('alt'))

            # Kata kunci yang ingin dicari
            keyword = "keyword utama"  # Ganti dengan kata kunci yang relevan

            # Cari kata kunci dalam konten body
            keyword_found = []
            if keyword.lower() in content.lower():
                keyword_found.append(keyword)

            # Proses pencarian kata kunci teratas
            stop_words = set(stopwords.words('indonesian') + stopwords.words('english'))
            words = re.findall(r'\b\w+\b', content.lower())
            filtered_words = [word for word in words if word not in stop_words]
            word_counts = Counter(filtered_words)
            keywords = word_counts.most_common(10)  # Ambil 10 kata kunci teratas

            # Dictionary untuk menyimpan skor tiap kriteria
            criteria_scores = {}

            # Kriteria 1: Title Tag
            if 50 <= title_length <= 60:
                criteria_scores['Title Length'] = 10
            elif 45 <= title_length < 50 or 60 < title_length <= 65:
                criteria_scores['Title Length'] = 5
            else:
                criteria_scores['Title Length'] = 0

            # Kriteria 2: Heading Tag
            if 2 <= heading_count <= 3:
                criteria_scores['Heading Count'] = 10
            elif heading_count == 1:
                criteria_scores['Heading Count'] = 5
            else:
                criteria_scores['Heading Count'] = 0

            # Kriteria 3: Panjang heading
            criteria_scores['Heading Length'] = 0
            for h in headings:
                h_length = len(h.get_text())
                if 20 <= h_length <= 70:
                    criteria_scores['Heading Length'] += 10
                elif 15 <= h_length < 20:
                    criteria_scores['Heading Length'] += 5

            # Kriteria 4: Keyword di Judul
            if title.lower().count(keyword.lower()) == 1:
                criteria_scores['Keyword in Title'] = 10
            elif title.lower().count(keyword.lower()) == 2:
                criteria_scores['Keyword in Title'] = 5
            else:
                criteria_scores['Keyword in Title'] = 0

            # Kriteria 5: Keyword di Paragraf Pertama
            first_paragraph = content.split('\n')[0]
            if first_paragraph.lower().count(keyword.lower()) in [1, 2]:
                criteria_scores['Keyword in First Paragraph'] = 10
            elif first_paragraph.lower().count(keyword.lower()) == 3:
                criteria_scores['Keyword in First Paragraph'] = 5
            else:
                criteria_scores['Keyword in First Paragraph'] = 0

            # Kriteria 6: Panjang Konten
            word_count = len(content.split())
            criteria_scores['Content Length'] = 10 if 300 <= word_count <= 500 else 0

            # Kriteria 7: Alt Tag pada Gambar
            if len(images) > 0:
                if alt_count == len(images):
                    criteria_scores['Alt Tag on Images'] = 10
                elif alt_count > 0:
                    criteria_scores['Alt Tag on Images'] = 5
                else:
                    criteria_scores['Alt Tag on Images'] = 0

            # Kriteria 8: Meta Tag
            if 0 <= meta_length <= 160 and keyword in meta_content:
                criteria_scores['Meta Tag'] = 10
            elif 0 <= meta_length <= 160:
                criteria_scores['Meta Tag'] = 5
            else:
                criteria_scores['Meta Tag'] = 0

            # Kriteria 9: Internal Links
            internal_links = soup.find_all('a', href=True)
            if any(link['href'].startswith('/') for link in internal_links):
                criteria_scores['Internal Links'] = 10
            else:
                criteria_scores['Internal Links'] = 0

            # Kriteria 10: Eksternal Link
            external_links = [link for link in internal_links if not link['href'].startswith('/')]
            criteria_scores['External Links'] = 10 if external_links else 0

            # Hitung total skor
            total_score = sum(criteria_scores.values())

            # Siapkan data untuk dikirim ke template
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
            return render(request, 'analysis-url.html', {'error': str(e)})

    return render(request, 'analysis-url.html')

def FAQ(request):
    return render(request, 'faq.html')