from django.shortcuts import render

# Create your views here.
def LandingPage(request):
    return render(request, 'landingpage.html')

def AnalysisURL(request):
    return render(request, 'analysis-url.html')

def RecommendationURL(request):
    return render(request, 'recommendation-url.html')

