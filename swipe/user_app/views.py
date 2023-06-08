from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from .models import Notaries, User, Message, Subscription, UserRequest
from .permissions import AllWhoVerified, IsOwnerOrReadOnly, IsOwner, IsUser, IsManager
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response



@extend_schema(tags=['Subscription'])
class SubscriptionGet(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user__id=user.id)

@extend_schema(tags=['Subscription'])
class SubscriptionCreate(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    http_method_names = ['post']

@extend_schema(tags=['Subscription'])
class SubscriptionUpdate(UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    http_method_names = ['put']

    def get_object(self):
        user = self.request.user
        subscription = user.subscription  # Получение подписки связанной с пользователем
        if not subscription:
            raise Http404('Подписка не найдена.')
        return subscription

    @action(detail=False, methods=['put'])
    def subscription_update(self, request):
        subscription = self.get_object()
        serializer = self.get_serializer(subscription, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['Notaries'])
class NotariesViewSet(viewsets.ModelViewSet):
    queryset = Notaries.objects.all()
    serializer_class = NotariesSerializer

@extend_schema(tags=['Message'])
class BaseMessage(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer



class MessageViewSet(BaseMessage):
    http_method_names = ['get', 'post', 'delete']
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user)

class MessageUserGet(BaseMessage):
    http_method_names = ['get']
    def get_queryset(self):
        user = self.kwargs['pk']
        return Message.objects.filter(sender=user)


@extend_schema(tags=['ManagerUserView'])
class UserRequestList(ListAPIView):
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer
    http_method_names = ['get']
    permission_classes = (IsManager,)


@extend_schema(tags=['ManagerUserView'])
class ManagerUserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ManagerUserListSerializer
    http_method_names = ['get']
    permission_classes = (IsManager,)


@extend_schema(tags=['ManagerUserView'])
class BlackListUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = BlackListSerializer
    http_method_names = ['put']
    permission_classes = (IsManager,)


@extend_schema(tags=['AdminCreate'])
class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminUser,)

@extend_schema(tags=['UserOwner'])
class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

@extend_schema(tags=['UserOwner'])
class OwnerRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

@extend_schema(tags=['UserOwner'])
class BaseViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(User, id=user.id)
        self.check_object_permissions(self.request, obj)
        return obj
    @action(detail=False, methods=['put'])
    def user_update(self, request):
        user = self.request.user
        data = request.data
        data['id'] = user.id
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserViewSet(BaseViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsUser,)


class OwnerViewSet(BaseViewSet):
    serializer_class = OwnerSerializer
    permission_classes = (IsOwner,)



