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

# Get details about all users strafbakken
def get_strafbakken():
  strafbakkenCount = list(Strafbak.objects.filter(active=True).values_list('receiver__username').annotate(strafbakken=Count('receiver')))
  users = list(User.objects.exclude(username='ibs').values_list('username', 'nickname').order_by('became_member', 'became_aspiring_member', 'first_drink_invited_at', 'nickname', 'username'))
  print(users)
  res = []
  for user in users:
    for strafbak in strafbakkenCount:
      if user[0] == strafbak[0]:
        res.append({'username': user[0], 'nickname': user[1], 'strafbakken': strafbak[1]})
        break
    else:
      res.append({'username': user[0], 'nickname': user[1], 'strafbakken': 0})
  return Response(res, status=status.HTTP_200_OK)

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
  strafbak = strafbakken[0]
  strafbak.active = 0
  strafbak.save()
  return Response(status=status.HTTP_200_OK)

# Get details of a user's strafbakken by name
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def strafbakken_user(request, username):
  users = get_list_or_404(User, username=username)
  user = users[0].id

  match (request.method):
    case 'GET':
      # Get details about a user's strafbakken
      strafbakken = Strafbak.objects.filter(receiver_id=user, active=True).all()
      details = [{'giver': x.giver.username, 'reason': x.reason, 'date': x.date} for x in strafbakken]
      response = {'strafbakken': len(details), 'details': details}
      return Response(response, status=status.HTTP_200_OK)
    case 'DELETE':
      # Delete a user's strafbak
      strafbakken = Strafbak.objects.filter(receiver_id=user, active=True).order_by('date')
      if (len(strafbakken) == 0):
        return Response(status=status.HTTP_400_BAD_REQUEST)
      strafbak = strafbakken[0]
      strafbak.active = 0
      strafbak.save()
      return Response(status=status.HTTP_200_OK)
  return Response(status=status.HTTP_400_BAD_REQUEST)

# Get an overview of all user's bakken
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bakken(request):
  bakkenCount = Strafbak.objects.filter(active=False).annotate(name=F('receiver__username')).values('name').annotate(bakken=Count('receiver'))
  return Response(list(bakkenCount), status=status.HTTP_200_OK)

# Get details about a user's bakken
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bakken_user(request, username):
  user = get_object_or_404(User, username=username)

  bakken = Strafbak.objects.filter(receiver_id=user, active=False).all()
  details = [{'date': x.date, 'reason': x.reason, 'giver': x.giver.username} for x in bakken]
  response = {'bakken': len(bakken), 'details': details}
  return Response(response, status=status.HTTP_200_OK)