import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings

from .serializers import ActivitySerializer, ParticipantSerialzer
from .models import Activity, Participant

from ibs.users.serializers import CommitteeSerializer

from ibs.users.models import User, Committee
from ibs.tools.permissions import IsSenate, IsSuperAdmin, IsMember

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity(request):
  if request.method == 'GET':
    """
    Returns all activities
    """
    if request.user.is_aspiring_member():
      activities = Activity.objects.filter(members_only=False, is_active=True)
    else:
      activities = Activity.objects.filter(is_active=True)

    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsMember])
@transaction.atomic
def create_activity(request):
  if request.method == 'POST':
    """
    Creates a new activity
    """
    serializer = ActivitySerializer(data=request.data)

    organisation = Committee.objects.filter(id=request.data['organisation'])

    if serializer.is_valid():
      try:
        # Run everything in a transaction
        with transaction.atomic():
          activity = serializer.save()

          if len(organisation) > 0:
            organisation = organisation[0]
            activity.organisation = organisation
            activity.save()


          users = User.objects.filter(~Q(username=settings.DEFAULT_IBS_USER_USERNAME))
          # Create a Participant object for every user 
          for u in users:
            participant = Participant(user=u, activity=serializer.instance, present=False)
            participant.save()
    
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      except Exception as e:
        # If something goes wrong, the transaction is reverted and the error is returned
        return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_detail(request, activity_id):
  if request.method == 'GET':
    """
    Get a specific activity by id
    """
    try:
      activity = Activity.objects.get(id=activity_id)
      participants = Participant.objects.filter(activity=activity).all()
      ps = []

      for p in participants:
        u = User.objects.get(id=p.user.id)
        ps.append({
          'user': u.get_full_name(),
          'email': u.email,
          'present': p.present,
          'profile_picture': u.profile_picture.url if u.profile_picture else None,
          'user_id': u.id
        })

      activty_serializer = ActivitySerializer(activity)
      return Response({
        'activity': activty_serializer.data,
        'participants': ps,
      })
    except Activity.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
  

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsSenate | IsSuperAdmin])
def update_activity(request, activity_id):
  if request.method == 'PATCH':
    """
    Update an activity
    """
    try:
      activity = Activity.objects.get(id=activity_id)
      serializer = ActivitySerializer(activity, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Activity.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  elif request.method == 'DELETE':
    """
    Delete a specific activity by id
    """
    try:
      activity = Activity.objects.get(id=activity_id)
      activity.active = False
      activity.save()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Activity.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def participation(request, activity_id):
  print(request.method)
  if request.method == 'GET':

    participant = get_object_or_404(Participant, user=request.user, activity=activity_id)
    serializer = ParticipantSerialzer(participant, data=request.data, partial=True)
    if serializer.is_valid():
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'POST':

    participant = get_object_or_404(Participant, user=request.user, activity=activity_id)
    participant.present = request.data['present']
    participant.save()

    return Response(status=status.HTTP_200_OK)