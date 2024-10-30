from django.shortcuts import render

# Create your views here.
def LandingPage(request):
    return render(request, 'landingpage.html')

def AnalysisURL(request):
    return render(request, 'analysis-url.html')

def RecommendationURL(request):
    return render(request, 'recommendation-url.html')

def analysis_result(request):
    # Anda bisa menambahkan logika perhitungan skor di sini
    return render(request, 'analysis-result.html')

def content_recommendation(request):
    return render(request, 'content-recommendation.html')  # Pastikan membuat template ini