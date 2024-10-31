from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPage, name="home"),
    path('analysis/', views.AnalysisURL, name='analysis'),
    path('recommendation/', views.RecommendationURL, name="recommendation"),
    path('analysis-result/', views.analysis_result, name='analysis-result'),
]
