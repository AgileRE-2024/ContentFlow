from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage, name='landingpage'),
    path('analysis-result/', views.analysis_result, name='analysis-result'),
    path('content-recommendation/', views.content_recommendation, name='content-recommendation'),
]
