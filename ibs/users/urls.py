from django.urls import path, include
from rest_framework import routers
from ibs.users import views

app_name = 'users'

urlpatterns = [
  path(
    '', 
    views.get_user, 
    name='get-user'),
  path(
    '<int:user_id>/',
    views.get_user_by_id,
    name='get-user-by-id'),
  path(
    'update/',
    views.update_own_user,
    name='update-own-user'),
  path(
    'update/<int:user_id>/',
    views.update_user_by_id,
    name='update-user-by-id'),
]