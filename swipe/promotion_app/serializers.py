
import datetime
from datetime import timedelta
from rest_framework import serializers

from infrastructures_app.models import Apartment
from promotion_app.models import *




class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"

class PromotionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"
