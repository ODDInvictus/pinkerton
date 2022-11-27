from django.contrib import admin

from .models import Product, ProductCategory, AlcoholProduct, FoodProduct, Transaction, ContributionTransaction, SaleTransaction

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(AlcoholProduct)
admin.site.register(FoodProduct)
admin.site.register(Transaction)
admin.site.register(ContributionTransaction)
admin.site.register(SaleTransaction)