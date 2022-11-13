from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ibs.users.models import User
from ibs.financial.models import Product, ProductCategory, Transaction, AlcoholProduct
from ibs.financial.serializers import TransactionSerializer, ProductSerializer
from ibs.tools.permissions import IsSenate, IsSuperAdmin, IsKasCo


"""
All views that are accessible by anyone with an account
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_transactions_for_user(request):
  user = request.user
  transactions = Transaction.objects.filter(user=user).all()
  serializer = TransactionSerializer(transactions, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_products(request):
  products = Product.objects.all()
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)


"""
All views that are accessible by the Senate, Admins or the KasCo
"""

@api_view(['GET'])
@permission_classes([IsSenate, IsSuperAdmin, IsKasCo])
def get_all_transactions(request, user_id):
  user = User.objects.get(id=user_id)
  transactions = Transaction.objects.filter(user=user).all()
  serializer = TransactionSerializer(transactions, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

