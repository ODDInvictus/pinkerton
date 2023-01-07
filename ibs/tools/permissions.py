from rest_framework.permissions import BasePermission

def _check_committe(user, attr):
  try:
    check = getattr(user, attr)
    if not check:
      return False
    return check()
  except:
    return False

class IsSenate(BasePermission):
  """
  Allows access only to senate members.
  """
  def has_permission(self, request, view):
    return _check_committe(request.user, 'is_senaat')


class IsSuperAdmin(BasePermission):
  """
  Allows access only to super admins.
  """

  def has_permission(self, request, view):
    print(request.user.is_super_admin())
    return _check_committe(request.user, 'is_super_admin')


class IsColosseum(BasePermission):
  """
  Allows access only to members of the Colosseum committee.
  """
  def has_permission(self, request, view):
    return _check_committe(request.user, 'is_colosseum')


class IsICT(BasePermission):
  """
  Allows access only to members of the ICT committee.
  """
  def has_permission(self, request, view):
    return _check_committe(request.user, 'is_ict')


class IsKasCo(BasePermission):
  """
  Allows access only to members of the KasCo committee.
  """
  def has_permission(self, request, view):
    return _check_committe(request.user, 'is_financie')


class IsFinanCie(BasePermission):
  """
  Allows access only to members of the FinanCie committee.
  """
  def has_permission(self, request, view):
    return _check_committe(request.user, 'is_financie')


class IsMember(BasePermission):
  """
  Allows access only to members
  """
  def has_permission(self, request, view):
    return _check_committe(request.user, 'is_member')


class IsAspiringMember(BasePermission):
  """
  Allows access only to aspiring members
  """
  def has_permission(self, request, view):
    return _check_committe(request.user, 'is_aspiring_member')