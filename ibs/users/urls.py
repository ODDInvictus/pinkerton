from django.urls import path, include
from ibs.users import views

app_name = 'users'

urlpatterns = [
  path('', views.get_user, name='get-user'),
  path('all/', views.get_users, name='get-all-users'),
  path('create/', views.create_user, name='create-user'),
  path('<int:user_id>/', views.get_user_by_id, name='get-user-by-id'),
  path('update/', views.update_own_user, name='update-own-user'),
  path('update/<int:user_id>/', views.update_user_by_id, name='update-user-by-id'),
  path('committee/', views.get_committees, name='get-committees'),
]