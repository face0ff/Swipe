from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from promotion_app.models import Promotion
from promotion_app.serializers import *
from user_app.permissions import IsOwnerNew, IsUser, IsUserNew


@extend_schema(tags=['Promotion'])
class PromotionViewSet(PsqMixin, viewsets.ModelViewSet):
    # serializer_class = ApartmentSerializer
    queryset = Promotion.objects.all()
    http_method_names = ['get', 'put']

    psq_rules = {

        ('list', 'retrieve'): [
            Rule([AllowAny], PromotionSerializer),
        ],
        ('update'): [
            Rule([IsUserNew], PromotionUpdateSerializer)
        ],
        ('my_promo'): [
            Rule([IsUserNew], PromotionSerializer)
        ]
    }


    @extend_schema(request=PromotionUpdateSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(methods=['get'], detail=False, url_name='my', serializer_class=PromotionSerializer)
    def my_promo(self, request):
        queryset = Promotion.objects.filter(apartment__user_id=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
