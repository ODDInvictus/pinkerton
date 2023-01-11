from django.urls import path

from ibs.maluspunten import views

app_name = 'maluspunten'

urlpatterns = [
  path('', views.index, name='index'),
  path('gelukt/', views.success, name='success'),
  path('overzicht/', views.overview, name='overview')
]
