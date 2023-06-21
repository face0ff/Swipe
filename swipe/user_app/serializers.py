import datetime
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from checkerboard_app.models import Checkerboard
from infrastructures_app.models import Infrastructure
from .models import Notaries, User, Message, Subscription, UserRequest, UserFavoriteApartment, \
    UserFavoriteInfrastructure
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from dj_rest_auth.serializers import UserDetailsSerializer, LoginSerializer

from .tasks import test


class CustomLoginSerializer(LoginSerializer):
    username = None  # Отключаем поле username

class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        password = validated_data['password1']
        hashed_password = make_password(password)
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['email'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        user.password = hashed_password
        action = self.context['request'].path.split('/')[-2]
        if action == 'user_register':
            user.role = 'user'
        elif action == 'owner_register':
            user.role = 'owner'
            infrastructure = Infrastructure.objects.create(owner=user)
            checkerboard = Checkerboard.objects.create(infrastructure_id=infrastructure)
            checkerboard.save()
            infrastructure.save()
        user.save()

        if allauth_settings.EMAIL_VERIFICATION != allauth_settings.EmailVerificationMethod.MANDATORY:
            email = EmailAddress.objects.create(
                user_id=user.id,
                email=user.email,
                verified=False,
                primary=True)
            email.send_confirmation(self.context['request'])

        return user


class NotariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notaries
        fields = "__all__"


class UserRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text',)

    def create(self, validated_data):
        user = self.context['request'].user
        sender = User.objects.get(id=user.id)
        receiver = User.objects.get(role='manager')
        message = Message.objects.create(
            text=validated_data['text'],
            sender=sender,
            receiver=receiver
        )
        return message

    def __delete__(self, instance):
        if instance == self.context['request'].user:
            return instance




class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role')

    def create(self, validated_data):
        print(self.validated_data)
        is_admin = self.context['request'].user.is_staff
        if is_admin:
            password = validated_data['password']
            hashed_password = make_password(password)
            user = User.objects.create(
                username=validated_data['email'],
                email=validated_data['email'],
                password=hashed_password,
                role=validated_data['role'],
            )
            email = EmailAddress.objects.create(
                user_id=user.id,
                email=user.email,
                verified=True,
                primary=True
            )
            return user


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            hashed_password = make_password(password)
            validated_data['password'] = hashed_password
        instance = super().update(instance, validated_data)
        return instance


class UserUpdateSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ('avatar', 'last_name', 'first_name', 'telephone', 'notification', 'to_agent',
                  'agent_first_name', 'agent_last_name', 'agent_telephone', 'agent_email')


class OwnerUpdateSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ('last_name', 'first_name')

class ManagerUserListSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'telephone', 'email', 'black_list')

class BlackListSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ()

    def update(self, instance, validated_data):
        if not instance.black_list:
            validated_data['black_list'] = True
        else:
            validated_data['black_list'] = False
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['message'] = 'Операция прошла успешно'
        return data

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('paid_by', 'auto_renewal')

    def create(self, validated_data):
        user = self.context['request'].user
        if user.subscription:
            raise serializers.ValidationError("Подписка уже существует.")
        paid_by = datetime.date.today() + timedelta(days=5)
        print(paid_by)
        subscription = Subscription.objects.create(
            auto_renewal=validated_data['auto_renewal'],
            paid_by=paid_by
        )
        user = User.objects.get(id=user.id)
        user.subscription = subscription
        user.save()
        return subscription


class FavoriteApartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteApartment
        fields = ('id', 'apartment_id',)

    def create(self, validated_data):
        user = self.context['request'].user
        if UserFavoriteApartment.objects.filter(user_id= user, apartment_id=validated_data['apartment_id']).exists():
            raise ValidationError("Вы пытаетесь добавить туже квартирку второй раз")
        instance = UserFavoriteApartment.objects.create(user_id=user, apartment_id=validated_data['apartment_id'])
        return instance

class FavoriteInfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteInfrastructure
        fields = ('id', 'infrastructure_id',)

    def create(self, validated_data):
        user = self.context['request'].user
        if UserFavoriteInfrastructure.objects.filter(infrastructure_id=validated_data['infrastructure_id']).exists():
            raise ValidationError("Вы пытаетесь добавить тотже ЖК второй раз")
        instance = UserFavoriteInfrastructure.objects.create(user_id=user, infrastructure_id=validated_data['infrastructure_id'])
        return instance

