from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import ActivitySerializer
from .models import Activity

class ActivityViewSet(APIView):
  """
  API endpoint that allows activities to be viewed or edited.
  """
  permission_classes = [permissions.IsAuthenticated]
  queryset = Activity.objects.all().order_by('-date')

  def get(self, request):
    serializer = ActivitySerializer(self.queryset.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request):
    data = {
      'activity': request.data.get('activity') 
    }
    serializer = ActivitySerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      # Next create a Participant object for each person
      
      # TODO

      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityDetailViewSet(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get_obj(self, activity_id):
    try:
      return Activity.objects.get(pk=activity_id)
    except Activity.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  def get(self, request, activity_id):
    activity = self.get_obj(activity_id)
    if not activity:
      return Response(
        {"error": "Activity with id: {} does not exist".format(activity_id)},
        status=status.HTTP_404_NOT_FOUND
      )

    serializer = ActivitySerializer(activity)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def delete(self, request, activity_id):
    activity = self.get_obj(activity_id)
    if not activity:
      return Response(
        {"error": "Activity with id: {} does not exist".format(activity_id)},
        status=status.HTTP_404_NOT_FOUND
      )

    activity.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def patch(self, request, activity_id):
    """
    Update an activity
    """
    activity = self.get_obj(activity_id)

    print(vars(activity))

    if not activity:
      return Response(
        {"error": "Activity with id: {} does not exist".format(activity_id)},
        status=status.HTTP_404_NOT_FOUND
      )

    serializer = ActivitySerializer(activity, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
