from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, CommitteeSerializer, FunctionSerializer
from ibs.users.models import User, Function, Committee
from ibs.tools.permissions import IsSuperAdmin, IsSenate

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
  """
  Get the current authenticated user
  """
  user = request.user
  functions = Function.objects.filter(user=user).all()
  committees = [f.committee for f in functions]      

  user_serializer = UserSerializer(user)
  committee_serializer = CommitteeSerializer(committees, many=True)
  function_serializer = FunctionSerializer(functions, many=True)

  return Response({
    'user': user_serializer.data,
    'committees': committee_serializer.data,
    'functions': function_serializer.data
  })


@api_view(['GET'])
@permission_classes([IsSenate, IsSuperAdmin])
def get_user_by_id(request, user_id):
  """
  Returns a user by id
  """
  try:
    user = User.objects.get(id=user_id)
    functions = Function.objects.filter(user=user).all()
    committees = [f.committee for f in functions]      

    user_serializer = UserSerializer(user)
    committee_serializer = CommitteeSerializer(committees, many=True)
    function_serializer = FunctionSerializer(functions, many=True)
    return Response({
      'user': user_serializer.data,
      'committees': committee_serializer.data,
      'functions': function_serializer.data
    })
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_own_user(request):
  """
  Update the current authenticated user
  """
  user = request.user
  serializer = UserSerializer(user, data=request.data, partial=True)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsSenate, IsSuperAdmin])
def update_user_by_id(request, user_id):
  """
  Update a user by id
  """
  try:
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
