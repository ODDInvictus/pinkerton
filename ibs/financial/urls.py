from django.urls import path

from . import views

app_name = 'financial'

urlpatterns = [
  # Product Category
  path('product_categories/', views.get_all_product_categories, name='product_category_list'),
  path('product_categories/<int:category_id>/', views.get_product_category_with_products, name='product_category_detail'),
  # Product
  path('products/', views.get_all_products, name='product_list'),
  path('products/new/food/', views.new_food_product, name='product_new_food'),
  path('products/new/alcohol/', views.new_alcohol_product, name='product_new_alcohol'),
  path('products/<int:product_id>/', views.get_product, name='product_detail'),
  # Transaction
  path('transactions/', views.get_all_transactions_for_user, name='transaction_list'),
  path('transactions/all/', views.get_all_transactions, name='transaction_list_all'),
  path('transactions/new/sale/', views.new_sale_transaction, name='transaction_new_sale'),
  path('transactions/new/generic/', views.new_generic_transaction, name='transaction_new_generic'),  
  path('transactions/new/contribution/', views.contribution, name='transaction_new_contribution'),
]