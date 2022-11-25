from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status, generics, permissions, serializers
from knox.models import AuthToken

from .serializers import UserSerializer, CommitteeSerializer, CommitteeMemberSerializer, LoginSerializer
from ibs.users.models import User, CommitteeMember, Committee
from ibs.tools.permissions import IsSuperAdmin, IsSenate

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
@permission_classes([IsSenate, IsSuperAdmin])
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


@api_view(['POST'])
@permission_classes([IsSenate, IsSuperAdmin])
def create_user(request):
  """
  Create a new user
  """
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
AUTHENTICATION views
"""

@api_view(['POST'])
def check_if_token_is_valid(token):
  """
  Check if a token is valid
  """
  try:
    token = AuthToken.objects.get(token=token)
    if token.expiry is not None and token.expiry < timezone.now():
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_200_OK)
  except AuthToken.DoesNotExist:
    return Response(status=status.HTTP_401_UNAUTHORIZED)


class SignInAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer
  permission_classes = [AllowAny]

  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    print(user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": AuthToken.objects.create(user)[1]
    })
