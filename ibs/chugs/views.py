from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from django.db import transaction
from django.db.models import Count
from django.db.models import F

from ibs.users.models import User

from ibs.chugs.models import Strafbak
from ibs.chugs.serializers import StrafbakSerializer

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def strafbakken(request):
  match request.method:
    case 'GET':
      return get_strafbakken()
    case 'POST':
      return give_strafbak(request)
    case 'DELETE':
      return trek_strafbak(request)
  return Response(status=status.HTTP_400_BAD_REQUEST)

# Get details about your strafbakken
def get_strafbakken():
  try:
    strafbakkenCount = Strafbak.objects.filter(active=True).annotate(name=F('receiver__username')).values('name').annotate(bakken=Count('receiver'))
    return Response(list(strafbakkenCount), status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Give a strafbak
def give_strafbak(request):
  request.data['giver'] = request.user.id

  try:
    users = User.objects.filter(username=request.data['receiver'])
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  if (len(users) == 0):
      return Response(status=status.HTTP_400_BAD_REQUEST)
  request.data['receiver'] = users[0].id

  serializer = StrafbakSerializer(data=request.data)
  if serializer.is_valid():
    try:
      serializer.save()
      return Response(status=status.HTTP_200_OK)
    except Exception as error:
      print(error)
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  return Response(status=status.HTTP_400_BAD_REQUEST)

# Delete a strafbak of the sender of the requets
def trek_strafbak(request):
  try:
    strafbak = Strafbak.objects.filter(receiver=request.user.id, active=True).order_by('date')[0]
    strafbak.active = 0
    strafbak.save()
    return Response(status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get details of a user's strafbakken by name
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def strafbakken_user(request, username):
  try:
    users = User.objects.filter(username=username)
    if (len(users) == 0):
      return Response(status=status.HTTP_400_BAD_REQUEST)
    user = users[0].id
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  match (request.method):
    case 'GET':
      # Get details about a user's strafbakken
      try:
        strafbakken = Strafbak.objects.filter(receiver_id=user, active=True).all()
        details = [{'giver': x.giver.username, 'reason': x.reason, 'date': x.date} for x in strafbakken]
        response = {'strafbakken': len(details), 'details': details}
        return Response(response, status=status.HTTP_200_OK)
      except Exception as error:
        print(error)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    case 'DELETE':
      # Delete a user's strafbak
      try:
        strafbakken = Strafbak.objects.filter(receiver_id=user, active=True).order_by('date')
        if (len(strafbakken) == 0):
          return Response(status=status.HTTP_400_BAD_REQUEST)
        strafbak = strafbakken[0]
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
def bakken_user(request, username):
  try:
    users = User.objects.filter(username=username)
    if (len(users) == 0):
      return Response(status=status.HTTP_400_BAD_REQUEST)
    user = users[0].id
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  try:
    bakken = Strafbak.objects.filter(receiver_id=user, active=False).all()
    details = [{'date': x.date, 'reason': x.reason, 'giver': x.giver.username} for x in bakken]
    response = {'bakken': len(bakken), 'details': details}
    return Response(response, status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)