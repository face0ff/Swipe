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