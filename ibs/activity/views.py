from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import transaction

from .serializers import ActivitySerializer
from .models import Activity, Participant

from ibs.users.models import User
from ibs.tools.permissions import IsSenate, IsSuperAdmin, IsMember

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity(request):
  if request.method == 'GET':
    """
    Returns all activities
    """
    activities = Activity.objects.all()
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
    if serializer.is_valid():
      try:
        # Run everything in a transaction
        with transaction.atomic():
          users = User.objects.all()
          serializer.save()

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
      serializer = ActivitySerializer(activity)
      return Response(serializer.data)
    except Activity.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
  

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsSenate, IsSuperAdmin])
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
      activity.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Activity.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)