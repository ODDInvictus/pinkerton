from django.contrib.auth.middleware import RemoteUserMiddleware

class DisableCSRFMiddleware(object):

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    setattr(request, '_dont_enforce_csrf_checks', True)
    response = self.get_response(request)
    return response
  
  
class PersistentHttpRemoteUserMiddleware(RemoteUserMiddleware):
  header = 'HTTP_REMOTE_USER'
  # force_logout_if_no_header = False