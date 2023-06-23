from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from checkerboard_app.models import Checkerboard, Floor, Riser
from infrastructures_app.models import Infrastructure


class CheckerboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkerboard
        fields = "__all__"



class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        infrastructure = Infrastructure.objects.get(owner_id=user)
        section_id = validated_data['section_id'].id
        number = validated_data['number']
        if Floor.objects.filter(section_id__corp_id=section_id, number=number).exists():
            raise ValidationError("Такой номер этажа уже используеться в данной секции")
        if not infrastructure.corp_set.filter(section=section_id).exists():
            raise ValidationError("Вы пытаетесь создать этаж не в своей секции")
        floor = Floor.objects.create(**validated_data)
        return floor

class RiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riser
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        infrastructure = Infrastructure.objects.get(owner_id=user)
        section_id = validated_data['section_id'].id
        number = validated_data['number']
        if Riser.objects.filter(section_id__corp_id=section_id, number=number).exists():
            raise ValidationError("Такой номер стояка уже используеться в данной секции")
        if not infrastructure.corp_set.filter(section=section_id).exists():
            raise ValidationError("Вы пытаетесь создать стояк не в своей секции")
        riser = Riser.objects.create(**validated_data)
        return riser