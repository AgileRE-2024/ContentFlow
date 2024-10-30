from django.shortcuts import render

def LandingPage(request):
    return render(request, 'landingpage.html')

def analysis_result(request):
    # Anda bisa menambahkan logika perhitungan skor di sini
    return render(request, 'analysis-result.html')

def content_recommendation(request):
    return render(request, 'content-recommendation.html')  # Pastikan membuat template ini
