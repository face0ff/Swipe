from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser

from .models import Notaries, User
from .permissions import AllWhoVerified
from .serializers import NotariesSerializer, UserSerializer, UserAdminSerializer, OwnerSerializer, \
    CustomRegisterSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


@extend_schema(tags=['Notaries'])
class NotariesViewSet(viewsets.ModelViewSet):
    queryset = Notaries.objects.all()
    serializer_class = NotariesSerializer


@extend_schema(tags=['AdminCreate'])
class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminUser,)


@extend_schema(tags=['UserUpdate'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['put']


@extend_schema(tags=['OwnerUpdate'])
class OwnerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = OwnerSerializer
    http_method_names = ['put']

@extend_schema(tags=['UserRegister'])
class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    http_method_names = ['post']

@extend_schema(tags=['OwnerRegister'])
class OwnerRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    http_method_names = ['post']
