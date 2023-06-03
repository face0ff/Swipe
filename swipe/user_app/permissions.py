from allauth.account.models import EmailAddress
from rest_framework import permissions


class AllWhoVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                email = EmailAddress.objects.get(user=request.user)
                return email.verified
            except EmailAddress.DoesNotExist:
                return False
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.id == request.user.id and request.user.role == request.path.split('/')[3].split('_')[0]:
            return True
        return False


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user'

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'