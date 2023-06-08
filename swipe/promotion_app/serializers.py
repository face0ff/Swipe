
import datetime
from datetime import timedelta
from rest_framework import serializers

from promotion_app.models import *


class PromotionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"

class PromotionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"

    def update(self, instance, validated_data):
        instance = self.Meta.model()
        instance.save()
        return instance

