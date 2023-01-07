from django.urls import path
from ibs.chugs import views

app_name = 'chugs'

urlpatterns = [
  path('strafbakken/', views.strafbakken),
  path('bakken/', views.bakken),
  path('strafbakken/<str:username>', views.strafbakken_user),
  path('bakken/<str:username>', views.bakken_user)
]