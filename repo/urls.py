from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_form, name='search_form'),
    path('results/', views.search_results, name='search_results'),
]
