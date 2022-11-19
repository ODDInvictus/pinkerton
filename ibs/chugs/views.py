from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([])
def bakken(request):
  match request.method:
    case 'GET':
      return get_bakken(request)
    case 'POST':
      return give_bakken(request)
    case 'DELETE':
      return trek_bakken(request)

def get_bakken(request):
  return Response('get', status=status.HTTP_200_OK)

def give_bakken(request):
  return Response('post', status=status.HTTP_200_OK)

def trek_bakken(request):
  return Response('delete', status=status.HTTP_200_OK)