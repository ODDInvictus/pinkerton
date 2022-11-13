from rest_framework import serializers

from .models import Product, ProductCategory, AlcoholProduct, Transaction, ContributionTransaction, SaleTransaction, AlcoholSaleTransaction


class ProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
  
  class Meta:
    model = ProductCategory
    fields = "__all__"


class AlcoholProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = AlcoholProduct
    fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):

  class Meta:
    model = Transaction
    fields = "__all__"


class SaleTransactionSerializer(serializers.ModelSerializer):

  class Meta:
    model = SaleTransaction
    fields = "__all__"


class AlcoholSaleTransactionSerializer(serializers.ModelSerializer):

  class Meta:
    model = AlcoholSaleTransaction
    fields = "__all__"


class ContributionTransactionSerializer(serializers.ModelSerializer):

  class Meta:
    model = ContributionTransaction
    fields = "__all__"

