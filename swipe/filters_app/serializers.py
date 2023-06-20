
import datetime
from datetime import timedelta
from rest_framework import serializers

from filters_app.models import Filter


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        exclude = ['user_id']

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user_id'] = user
        return attrs

    def create(self, validated_data):
        filter = Filter.objects.create(**validated_data)
        return filter

