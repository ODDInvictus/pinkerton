from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from django.db import transaction
from django.db.models import Count

from ibs.chugs.models import Strafbak, Anytimer, Chug
from ibs.chugs.serializers import StrafbakSerializer, ChugSerializer

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def bakken(request):
  match request.method:
    case 'GET':
      return get_bakken(request)
    case 'POST':
      return give_bakken(request)
    case 'DELETE':
      return trek_bakken(request)

def get_bakken(request):
  try:
    bakkenCount = Strafbak.objects.raw('''
      SELECT u.username AS name, COUNT(s.receiver_id) AS bakken, s.id
      FROM users_user AS u, chugs_strafbak AS s
      WHERE u.id = s.receiver_id
      GROUP BY s.receiver_id
      ORDER BY bakken
    ''')
    response = [{'Name': x.name, 'Bakken': x.bakken} for x in bakkenCount]
    return Response(response, status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def give_bakken(request):
  request.data['giver'] = request.user.id
  serializer = StrafbakSerializer(data=request.data)
  if serializer.is_valid():
    try:
      with transaction.atomic():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as error:
      print(error)
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  return Response(status=status.HTTP_400_BAD_REQUEST)

def trek_bakken(request):
  serializer = ChugSerializer(data={'user': request.user.id})
  if serializer.is_valid():
    try:
      with transaction.atomic():
        serializer.save()
        bak = Strafbak.objects.filter(receiver=request.user.id).order_by('date')[0]
        bak.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as error:
      print(error)
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  return Response(status=status.HTTP_400_BAD_REQUEST)