from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from .serializers import UserSerializer, CommitteeSerializer, CommitteeMemberSerializer, LoginSerializer
from ibs.users.models import User, CommitteeMember, Committee
from ibs.tools.permissions import IsFinanCie, IsKasCo, IsSuperAdmin, IsSenate

from datetime import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
  """
  Get the current authenticated user
  """
  user = request.user
  functions = CommitteeMember.objects.filter(user=user).all()
  committees = [f.committee for f in functions]      

  user_serializer = UserSerializer(user)
  committee_serializer = CommitteeSerializer(committees, many=True)
  commitee_member_serializer = CommitteeMemberSerializer(functions, many=True)

  return Response({
    'user': user_serializer.data,
    'committees': committee_serializer.data,
    'committee_members': commitee_member_serializer.data
  })


@api_view(['GET'])
@permission_classes([IsSenate | IsSuperAdmin])
def get_user_by_id(request, user_id):
  """
  Returns a user by id
  """
  try:
    user = User.objects.get(id=user_id)
    functions = CommitteeMember.objects.filter(user=user).all()
    committees = [f.committee for f in functions]      

    user_serializer = UserSerializer(user)
    committee_serializer = CommitteeSerializer(committees, many=True)
    commitee_member_serializer = CommitteeMemberSerializer(functions, many=True)
    return Response({
      'user': user_serializer.data,
      'committees': committee_serializer.data,
      'committee_members': commitee_member_serializer.data
    })
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsSenate | IsSuperAdmin])
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


@api_view(['POST'])
@permission_classes([IsSenate | IsSuperAdmin])
def create_user(request):
  """
  Create a new user
  """
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_committees(request):
  """
  Get all committees
  """
  committees = Committee.objects.all()
  serializer = CommitteeSerializer(committees, many=True)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsSenate | IsSuperAdmin | IsFinanCie])
def get_users(request):
  """
  Get all users
  """
  users = User.objects.all()

  filter = [u for u in users if u.is_member() == True or u.is_aspiring_member() == True]

  serializer = UserSerializer(filter, many=True)
  return Response(serializer.data)
