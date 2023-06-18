import hashlib
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import ListField, ImageField, empty
from checkerboard_app.serializers import FloorSerializer, RiserSerializer
from infrastructures_app.models import Infrastructure, Corp, Section, Image, Apartment, ImageApart, News, Docs
from promotion_app.models import Promotion
from user_app.models import User, UserRequest


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


class EmptyBase64ImageField(Base64ImageField):
    def run_validation(self, data=empty):
        if not data.startswith('data:image'):
            return data
        return super().run_validation(data)


class ImagesSerializer(serializers.ModelSerializer):
    image = EmptyBase64ImageField(required=False)
    image_delete = serializers.BooleanField(required=False)

    class Meta:
        model = Image
        fields = ('image', 'image_place', 'image_delete')


class InfrastructureUpDelSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    images = ImagesSerializer(many=True, source='imageInfrastructure')
    photo = EmptyBase64ImageField(required=False)

    class Meta:
        model = Infrastructure
        fields = "__all__"

    def update(self, instance, validated_data):

        images_data = validated_data.pop('imageInfrastructure', [])
        if isinstance(validated_data['photo'], str):
            validated_data.pop('photo', None)

        instance = super().update(instance, validated_data)

        hash_list = list(Image.objects.filter(infrastructure_id=instance).values_list('hash', flat=True))

        for image_data in images_data:
            image_file = image_data.get('image', None)
            if not isinstance(image_file, str):
                with image_file as file:
                    image_content = file.read()
                    image_hash = hashlib.sha256(image_content).hexdigest()
                    if image_hash in hash_list:
                        continue

                    Image.objects.create(
                        infrastructure_id=instance,
                        image=image_file,
                        image_place=image_data.get('image_place'),
                        hash=image_hash
                    )

            if image_data.get('image_delete'):
                Image.objects.filter(image_place=image_data.get('image_place')).delete()

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

    def validate(self, attrs):
        print(attrs)
        return attrs


class ApartmentSerializer(serializers.ModelSerializer):
    images = ImageApartSerializer(many=True, source='imageApart', read_only=True)
    floor_id = FloorSerializer(read_only=True)
    riser_id = RiserSerializer(read_only=True)

    class Meta:
        model = Apartment
        fields = "__all__"


class ApartmentBaseSerializer(serializers.ModelSerializer):
    images = ListField(child=ImageField(max_length=100000, allow_empty_file=False, use_url=False), write_only=True)
    image_places = serializers.CharField(required=False)

    class Meta:
        model = Apartment
        fields = ('schema', 'images', 'image_places', 'infrastructure_id', 'riser_id', 'floor_id', 'view', 'technology',
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
        image_places = [int(place) for place in validated_data.pop('image_places', '').split(',')]
        promotion = Promotion.objects.create()
        validated_data['promotion_id'] = promotion.id
        validated_data['user_id'] = self.context['request'].user
        apartment = Apartment.objects.create(**validated_data)
        ImageApart.objects.filter(image_place__in=image_places).delete()
        UserRequest.objects.create(infrastructure_id=validated_data['infrastructure_id'], apartment_id=apartment)
        for image_data in uploaded_images:
            ImageApart.objects.create(apartment_id=apartment, image=image_data,
                                      image_place=image_places[uploaded_images.index(image_data)])
        return apartment


class ApartmentUpdateSerializer(ApartmentBaseSerializer):
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('images', [])
        image_places = [int(place) for place in validated_data.pop('image_places', '').split(',')]
        instance = super().update(instance, validated_data)
        ImageApart.objects.filter(image_place__in=image_places).delete()
        for image_data in uploaded_images:
            ImageApart.objects.create(apartment_id=instance, image=image_data,
                                      image_place=image_places[uploaded_images.index(image_data)])
        return instance


class AcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ('accept', 'rejection')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("news_description",)

    def create(self, validated_data):
        user = self.context['request'].user
        infra_id = Infrastructure.objects.get(owner=user)
        validated_data['infrastructure_id'] = infra_id
        news = News.objects.create(**validated_data)
        return news


class DocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docs
        fields = "__all__"


class DocsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docs
        fields = ("file", "is_excel")

    def create(self, validated_data):
        user = self.context['request'].user
        infra_id = Infrastructure.objects.get(owner=user)
        validated_data['infrastructure_id'] = infra_id
        docs = Docs.objects.create(**validated_data)
        return docs
