from django.urls import path
from ibs.chugs import views

app_name = 'chugs'

urlpatterns = [
  path('', views.bakken)
]