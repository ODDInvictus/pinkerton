from django.urls import path, include
from rest_framework import routers
from ibs.activity import views

app_name = 'activity'

urlpatterns = [
  path('', views.ActivityViewSet.as_view(), name='activity'),
  path('<int:activity_id>/', views.ActivityDetailViewSet.as_view(), name='activity-detail'),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]