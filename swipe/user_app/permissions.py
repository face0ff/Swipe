from allauth.account.models import EmailAddress
from rest_framework import permissions

from checkerboard_app.models import Floor, Riser
from infrastructures_app.models import Corp, Section, Infrastructure, Apartment
from user_app.models import User


class IsOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'owner':
            return True


class IsUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'user':
            return True

class IsManager(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'manager':
            return True



class IsManagerOrOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Corp):
            user_corps = request.user.infrastructure.corp_set.all()
            if obj in user_corps and request.user.role == 'owner' or request.user.role == 'manager':
                return True
            return False
        if isinstance(obj, Section):
            user_corps = request.user.infrastructure.corp_set.all()
            if obj.corp_id in user_corps and (request.user.role == 'owner' or request.user.role == 'manager'):
                return True
            return False
        if isinstance(obj, Floor):
            user_corps = request.user.infrastructure.corp_set.all()
            corps_sections = Section.objects.filter(corp_id__in=user_corps)
            if obj.section_id in corps_sections and (request.user.role == 'owner' or request.user.role == 'manager'):
                return True
            return False
        if isinstance(obj, Riser):
            user_corps = request.user.infrastructure.corp_set.all()
            corps_sections = Section.objects.filter(corp_id__in=user_corps)
            if obj.section_id in corps_sections and (request.user.role == 'owner' or request.user.role == 'manager'):
                return True
            return False
        if isinstance(obj, Infrastructure):
            user_infrastructure = request.user.infrastructure
            if obj == user_infrastructure and (request.user.role == 'owner' or request.user.role == 'manager'):
                return True
            return False
        if isinstance(obj, Apartment):
            user_apartments = request.user.infrastructure.apartment_set.all()
            if obj in user_apartments:
                return True
            return False

class IsOwnerNew(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.infrastructure_id.owner

class IsUserNew(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user_apart = User.objects.get(infrastructure__apartment__promotion_id=obj.id)
        return request.user == user_apart


class IsUserFavor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user_id