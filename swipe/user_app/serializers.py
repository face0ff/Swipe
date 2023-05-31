import base64
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Notaries, User
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from dj_rest_auth.serializers import UserDetailsSerializer, LoginSerializer


class CustomLoginSerializer(LoginSerializer):
    username = None  # Отключаем поле username

class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        password = validated_data['password1']
        hashed_password = make_password(password)
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['email'])
        user.password = hashed_password
        action = self.context['request'].path.split('/')[-2]
        if action == 'user_register':
            user.role = 'user'
        elif action == 'owner_register':
            user.role = 'owner'
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


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        print(self.validated_data)
        is_admin = self.context['request'].user.is_staff
        if is_admin:
            password = validated_data['password']
            hashed_password = make_password(password)
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                password=hashed_password,
            )
            email = EmailAddress.objects.create(
                user_id=user.id,
                email=user.email,
                verified=True,
                primary=True
            )
            return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'avatar', 'email', 'password', 'last_name', 'first_name')

    def update(self, instance, validated_data):
        print('23423234234')
        avatar_data = validated_data.get('avatar')
        print(avatar_data)
        if avatar_data:
            decoded_image = base64.b64decode(avatar_data)
            avatar_file = ContentFile(decoded_image)
            avatar_file.name = 'avatar.jpg'
            instance.avatar.save('avatar.jpg', avatar_file, save=True)
        instance.role = 'owner'

        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        return self.update(instance, validated_data)
