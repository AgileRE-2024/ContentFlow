from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPage, name=""),
    path('analysis/', views.AnalysisURL, name=""),
    path('recommendation/', views.RecommendationURL, name=""),
    path('analysis-result/', views.analysis_result, name='analysis-result'),
    path('content-recommendation/', views.content_recommendation, name='content-recommendation'),
]
