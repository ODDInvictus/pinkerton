from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ibs.users.models import User
from ibs.financial.models import Product, ProductCategory, FoodProduct, AlcoholProduct, Transaction, SaleTransaction, ContributionTransaction
from ibs.financial.serializers import TransactionSerializer, ProductSerializer, ProductCategorySerializer, AlcoholProductSerializer, FoodProductSerializer, ContributionTransactionSerializer, SaleTransactionSerializer
from ibs.tools.permissions import IsSenate, IsSuperAdmin, IsKasCo


"""
PRODUCT CATEGORY
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_product_categories(request):
  categories = ProductCategory.objects.all()
  serializer = ProductCategorySerializer(categories, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_category_with_products(request, category_id):
  category = ProductCategory.objects.get(id=category_id)
  products = Product.objects.filter(category=category).all()
  serializer = ProductCategorySerializer(category)
  return Response({
    'category': serializer.data,
    'products': ProductSerializer(products, many=True).data
  }, status=status.HTTP_200_OK)


"""
PRODUCTS
"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_products(request):
  products = Product.objects.all()
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, product_id):
  product = Product.objects.get(id=product_id)
  serializer = ProductSerializer(product)
  return Response(serializer.data, status=status.HTTP_200_OK)


"""
TRANSACTIONS
"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_transactions_for_user(request):
  transactions = Transaction.objects.filter(user=request.user).all()
  serializer = TransactionSerializer(transactions, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsSuperAdmin | IsSenate | IsKasCo])
def get_all_transactions(request):
  transactions = Transaction.objects.all()
  serializer = TransactionSerializer(transactions, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsKasCo | IsSenate | IsSuperAdmin])
def new_sale_transaction(request):
  try:
    data = request.data
    product = Product.objects.get(id=request.data['product'])

    data['price'] = product.price * request.data['amount']

    serializer = SaleTransactionSerializer(data=request.data)

    if serializer.is_valid():
      # serializer.save()

      return Response(serializer.data, status=status.HTTP_200_OK)
  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  except Exception as e:
    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsKasCo | IsSenate | IsSuperAdmin])
def new_generic_transaction(request):
  serializer = TransactionSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


