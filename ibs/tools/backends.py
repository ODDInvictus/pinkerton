from django.contrib.auth.backends import RemoteUserBackend

from ibs.users.models import User

class AutheliaRemoteUserAuthenticationBackend(RemoteUserBackend):
  create_unknown_user = False
  
  def authenticate(self, request, remote_user):
    if not remote_user:
      return None
    
    print('Authenticating user: ' + remote_user)
    
    # Just check if username exists, then return user
    try:
      user = User.objects.get(username=remote_user)
      
      if not user.is_active:
        return None
      
      return user
    except:
      print('User not found!')
      return None