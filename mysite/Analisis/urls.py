from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPage, name="home"),
    path('analysis/', views.AnalysisURL, name='analysis'),
    path('recommendation/', views.RecommendationURL, name="recommendation"),
    path('analysis-result/', views.AnalysisResult, name='analysis-result'),
    path('faq/', views.FAQ, name='faq'),
]
