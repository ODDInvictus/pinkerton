from rest_framework import serializers

from .models import Product, ProductCategory, AlcoholProduct, Transaction, ContributionTransaction, SaleTransaction, FoodProduct
from ibs.users.models import User

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

class FoodProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = FoodProduct
    fields = "__all__"


class TransactionSerializer(serializers.Serializer):
  date = serializers.DateField(format="%d-%m-%Y")
  description = serializers.CharField(max_length=512)
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  added_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

  def create(self, validated_data):
    return Transaction.objects.create(**validated_data)


class SaleTransactionSerializer(serializers.Serializer):
  date = serializers.DateField(format="%d-%m-%Y")
  description = serializers.CharField(max_length=512)
  added_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
  product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
  amount = serializers.IntegerField()
  price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

  def create(self, validated_data):
    trans = SaleTransaction.objects.create(**validated_data)
    product = validated_data['product']
    
    trans.price = product.price * validated_data['amount']

    trans.save()

    return trans



class ContributionTransactionSerializer(serializers.Serializer):
  date = serializers.DateField(format="%d-%m-%Y")
  description = serializers.CharField(max_length=512)
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  added_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

  def create(self, validated_data):
    return ContributionTransaction.objects.create(**validated_data)