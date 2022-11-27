from django.urls import path
from ibs.chugs import views

app_name = 'chugs'

urlpatterns = [
  path('strafbakken/', views.strafbakken),
  path('bakken/', views.bakken),
  path('strafbakken/<int:user>', views.strafbakken_user),
  path('bakken/<int:user>', views.bakken_user)
]