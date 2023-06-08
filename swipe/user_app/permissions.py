from allauth.account.models import EmailAddress
from rest_framework import permissions

from checkerboard_app.models import Floor
from infrastructures_app.models import Corp, Section


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

class IsManagerOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Corp):
            user_corps = request.user.infrastructure.corp_set.all()
            if obj in user_corps and request.user.role == 'owner' or request.user.role == 'manager':
                return True
            return False
        if isinstance(obj, Section):
            user_corps = request.user.infrastructure.corp_set.all()
            for i in user_corps:
                print(i)
            print(obj.corp_id)
            if obj.corp_id in user_corps and (request.user.role == 'owner' or request.user.role == 'manager'):
                return True
            return False
        if isinstance(obj, Floor):
            user_corps = request.user.infrastructure.corp_set.all()
            corps_sections = Section.objects.filter(corp_id__in=user_corps)
            if obj.section_id in corps_sections and (request.user.role == 'owner' or request.user.role == 'manager'):
                return True
            return False