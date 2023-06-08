from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView

from promotion_app.models import Promotion
from promotion_app.serializers import *


@extend_schema(tags=['Promotion'])
class PromotionUpdate(UpdateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionUpdateSerializer
    http_method_names = ['put']



@extend_schema(tags=['Promotion'])
class PromotionDelete(UpdateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionDeleteSerializer
    http_method_names = ['put']
