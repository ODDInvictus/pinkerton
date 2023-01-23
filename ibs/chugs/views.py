from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from django.db.models import Count
from django.db.models import F

from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404

from ibs.users.models import User

from ibs.chugs.models import Strafbak
from ibs.chugs.serializers import StrafbakSerializer

from datetime import datetime

# --- Strafbakken ---

# /strafbakken
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

# Get an overview of all users' bakken
def get_strafbakken():
  return Response(getCount(isActive=True), status=status.HTTP_200_OK)

# Give a strafbak
def give_strafbak(request):
  request.data['giver'] = request.user.id
  users = get_list_or_404(User, username=request.data['receiver'])
  if (len(users) == 0):
    return Response(status=status.HTTP_400_BAD_REQUEST)
  request.data['receiver'] = users[0].id

  serializer = StrafbakSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(status=status.HTTP_200_OK)
  return Response(status=status.HTTP_400_BAD_REQUEST)

# Delete a strafbak of the sender of the requets
def trek_strafbak(request):
  strafbakken = Strafbak.objects.filter(receiver=request.user.id, active=True).order_by('date')
  if (len(strafbakken) == 0):
    return Response(status=status.HTTP_400_BAD_REQUEST)
  deleteStrafbak(strafbakken[0])
  return Response(status=status.HTTP_200_OK)

# /strafbakken/<username>
# Get details of a user's strafbakken by name or delete a strafbak by name
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def strafbakken_user(request, username):
  users = get_list_or_404(User, username=username)
  user = users[0].id

  match (request.method):
    case 'GET':
      # Get details about a user's strafbakken
      strafbakken = Strafbak.objects.filter(receiver_id=user, active=True).all()
      details = [{
        'giver': x.giver.nickname or x.giver.username,
        'giver_username': x.giver.username,
        'reason': x.reason,
        'date': x.date
      } for x in strafbakken]
      response = {'bakken': len(details), 'details': details}
      return Response(response, status=status.HTTP_200_OK)
    case 'DELETE':
      # Delete a user's strafbak
      strafbakken = Strafbak.objects.filter(receiver_id=user, active=True).order_by('date')
      if (len(strafbakken) == 0):
        return Response(status=status.HTTP_400_BAD_REQUEST)
      deleteStrafbak(strafbakken[0])
      
      return Response(status=status.HTTP_200_OK)
  return Response(status=status.HTTP_400_BAD_REQUEST)

# --- Bakken ---

# /bakken
# Get an overview of all users' bakken
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bakken(request):
  return Response(getCount(isActive=False), status=status.HTTP_200_OK)

# /bakken/<username>
# Get details about a user's bakken
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bakken_user(request, username):
  user = get_object_or_404(User, username=username)
  bakken = Strafbak.objects.filter(receiver_id=user, active=False).all()
  details = [{
    'date': x.date_deleted,
    'reason': x.reason,
    'giver': x.giver.nickname or x.giver.username,
    'giver_username': x.giver.username,
    'dateReceived': x.date
  } for x in bakken]
  response = {'bakken': len(bakken), 'details': details}
  return Response(response, status=status.HTTP_200_OK)

# --- Helper functions ---

# Get a count of all users' active bakken (strafbakken) or inactive bakken (bakken)
def getCount(isActive):
  bakkenCount = list(Strafbak.objects.filter(active=isActive).values_list('receiver__username').annotate(strafbakken=Count('receiver')))
  users = list(User.objects.exclude(username='ibs').values_list('username', 'nickname').order_by('became_member', 'became_aspiring_member', 'first_drink_invited_at', 'nickname', 'username'))
  res = []
  for user in users:
    for bak in bakkenCount:
      if user[0] == bak[0]:
        res.append({
          'username': user[0],
          'nickname': user[1],
          'bakken': bak[1]
        })
        break
    else:
      res.append({
        'username': user[0],
        'nickname': user[1],
        'bakken': 0
      })
  return res

def deleteStrafbak(strafbak):
  strafbak.active = False
  strafbak.date_deleted = datetime.now()
  strafbak.save()