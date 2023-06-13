from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import ListField, ImageField
from rest_framework.serializers import ListSerializer

from checkerboard_app.serializers import FloorSerializer, RiserSerializer
from infrastructures_app.models import Infrastructure, Corp, Section, Image, Apartment, ImageApart
from promotion_app.models import Promotion
from user_app.models import User


class CorpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corp
        fields = "__all__"


class CorpCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corp
        fields = ('number',)

    def validate(self, attrs):
        user = self.context['request'].user
        infrastructure = Infrastructure.objects.get(owner=user)
        attrs['infrastructure_id'] = infrastructure
        return attrs

    def create(self, validated_data):
        infrastructure_id = validated_data['infrastructure_id'].id
        number = validated_data['number']
        if Corp.objects.filter(infrastructure_id=infrastructure_id, number=number).exists():
            raise ValidationError("Такой номер корпуса уже используеться в данной инфраструктуре")

        corp = Corp.objects.create(**validated_data)
        return corp


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        infrastructure = Infrastructure.objects.get(owner=user)
        corp_id = validated_data['corp_id']
        number = validated_data['number']
        if Section.objects.filter(corp_id=corp_id, number=number).exists():
            raise ValidationError("Такой номер секции уже используеться в данного корпуса")
        if corp_id not in infrastructure.corp_set.all():
            raise ValidationError("Вы пытаетесь создать секцию не в своем корпусе")
        section = Section.objects.create(**validated_data)
        return section


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class ImagesSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Image
        fields = ('image',)


class InfrastructureUpDelSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    images = ImagesSerializer(many=True, source='imageInfrastructure')
    photo = Base64ImageField(required=False)

    class Meta:
        model = Infrastructure
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.imageInfrastructure.all().delete()
        images_data = validated_data.pop('imageInfrastructure', [])
        instance = super().update(instance, validated_data)
        for image_data in images_data:
            Image.objects.create(infrastructure_id=instance, image=image_data['image'])
        return instance


class InfrastructureSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    images = ImagesSerializer(many=True, source='imageInfrastructure', read_only=True)
    photo = Base64ImageField(required=False, read_only=True)

    class Meta:
        model = Infrastructure
        fields = "__all__"


class ImageApartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)


class ApartmentSerializer(serializers.ModelSerializer):
    images = ImageApartSerializer(many=True, source='imageApart', read_only=True)
    floor_id = FloorSerializer(read_only=True)
    riser_id = RiserSerializer(read_only=True)

    class Meta:
        model = Apartment
        fields = "__all__"


class ApartmentBaseSerializer(serializers.ModelSerializer):
    images = ListField(child=ImageField(max_length=100000, allow_empty_file=False, use_url=False), write_only=True)

    class Meta:
        model = Apartment
        fields = ('schema', 'images', 'infrastructure_id', 'riser_id', 'floor_id', 'view', 'technology',
                  'apart_status', 'quantity', 'appointment',
                  'state', 'plane', 'area',
                  'kitchen_area', 'balcony', 'heating',
                  'payment', 'commission', 'communication',
                  'apart_description', 'price')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['images'] = [image.image.url for image in instance.imageApart.all()]
        return data


class ApartmentCreateSerializer(ApartmentBaseSerializer):
    def create(self, validated_data):
        uploaded_images = validated_data.pop('images', [])
        promotion = Promotion.objects.create()
        validated_data['promotion_id'] = promotion.id
        apartment = Apartment.objects.create(**validated_data)
        apartment.imageApart.all().delete()
        for image_data in uploaded_images:
            ImageApart.objects.create(apartment_id=apartment, image=image_data)
        return apartment


class ApartmentUpdateSerializer(ApartmentBaseSerializer):
    def update(self, instance, validated_data):
        instance.imageApart.all().delete()
        uploaded_images = validated_data.pop('images', [])
        instance = super().update(instance, validated_data)
        for image_data in uploaded_images:
            ImageApart.objects.create(apartment_id=instance, image=image_data)
        return instance

class AcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ('accept', 'rejection')


