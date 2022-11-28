from django.urls import path, include
from rest_framework import routers
from ibs.activity import views

app_name = 'activity'

urlpatterns = [
  path(
    '', 
    views.activity, 
    name='activity'),
  path(
    'calendar/',
    views.calendar,
    name='calendar'),
  path(
    'create/',
    views.create_activity,
    name='create-activity'),
  path(
    '<int:activity_id>/', 
    views.activity_detail, 
    name='activity-detail'),
  path(
    'update/<int:activity_id>/',
    views.update_activity,
    name='update-activity')
]