from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from django.db import transaction
from django.db.models import Count
from django.db.models import F

from ibs.chugs.models import Strafbak, Anytimer, Chug
from ibs.chugs.serializers import StrafbakSerializer, ChugSerializer

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def strafbakken(request):
  match request.method:
    case 'GET':
      return get_bakken()
    case 'POST':
      return give_bakken(request)
    case 'DELETE':
      return trek_bakken(request)
  return Response(status=status.HTTP_400_BAD_REQUEST)

# Get details about your strafbakken
def get_bakken():
  try:
    strafbakkenCount = Strafbak.objects.filter(active=True).annotate(name=F('receiver__username')).values('name').annotate(bakken=Count('receiver'))
    return Response(list(strafbakkenCount), status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Give a strafbak
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

# Delete a strafbak of the sender of the requets
def trek_bakken(request):
  try:
    with transaction.atomic():
      strafbak = Strafbak.objects.filter(receiver=request.user.id).order_by('date')[0]
      strafbak.active = 0
      strafbak.save()
      return Response(status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get details of a user's strafbakken by id
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def strafbakken_user(request, user):
  match (request.method):
    case 'GET':
      # Get details about a user's strafbakken
      try:
        strafbakken = Strafbak.objects.filter(receiver_id=user, active=True).all()
        details = [{'giver': x.giver_id, 'reason': x.reason, 'date': x.date} for x in strafbakken]
        response = {'strafbakken': len(details), 'details': details}
        return Response(response, status=status.HTTP_200_OK)
      except Exception as error:
        print(error)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    case 'DELETE':
      # Delete a user's strafbak
      try:
          with transaction.atomic():
            strafbak = Strafbak.objects.filter(receiver=user).order_by('date')[0]
            strafbak.active = 0
            strafbak.save()
            return Response(status=status.HTTP_200_OK)
      except Exception as error:
        print(error)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  return Response(status=status.HTTP_400_BAD_REQUEST)

# Get an overview of all user's bakken
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bakken(request):
  try:
    bakkenCount = Strafbak.objects.filter(active=False).annotate(name=F('receiver__username')).values('name').annotate(bakken=Count('receiver'))
    return Response(list(bakkenCount), status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get details about a user's bakken
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bakken_user(request, user):
  try:
    bakken = Strafbak.objects.filter(receiver=user, active=False).all()
    details = [{'date': x.date, 'reason': x.reason, 'giver': x.giver.username} for x in bakken]
    response = {'bakken': len(bakken), 'details': details}
    return Response(response, status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)