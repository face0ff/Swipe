from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from checkerboard_app.models import Checkerboard, Floor
from infrastructures_app.models import Infrastructure, Corp, Section



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
        corp_id = validated_data['corp_id'].id
        number = validated_data['number']
        if Section.objects.filter(corp_id=corp_id, number=number).exists():
            raise ValidationError("Такой номер секции уже используеться в данного корпуса")
        if corp_id not in infrastructure.corp_set.all():
            raise ValidationError("Вы пытаетесь создать секцию не в своем корпусе")
        section = Section.objects.create(**validated_data)
        return section
