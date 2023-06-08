from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView

from infrastructures_app.models import Corp, Section
from infrastructures_app.serializers import CorpCreateSerializer, CorpSerializer, SectionSerializer
from user_app.permissions import IsOwner, IsManager, IsManagerOrOwner


# Create your views here.
@extend_schema(tags=['Corp'])
class CorpViewSet(viewsets.ModelViewSet):
    queryset = Corp.objects.all()
    serializer_class = CorpSerializer
    http_method_names = ['get', 'delete']
    permission_classes = (IsManagerOrOwner,)

@extend_schema(tags=['Corp'])
class CorpList(ListAPIView):
    http_method_names = ['get']
    serializer_class = CorpSerializer
    permission_classes = (IsManagerOrOwner,)

    def get_queryset(self):
        user = self.request.user
        return Corp.objects.filter(infrastructure_id__owner=user)


@extend_schema(tags=['Corp'])
class CorpCreate(CreateAPIView):
    queryset = Corp.objects.all()
    serializer_class = CorpCreateSerializer
    http_method_names = ['post']
    permission_classes = (IsManagerOrOwner,)


@extend_schema(tags=['Section'])
class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsManagerOrOwner,)


@extend_schema(tags=['Section'])
class SectionList(ListAPIView):
    serializer_class = SectionSerializer
    http_method_names = ['get']
    permission_classes = (IsManagerOrOwner,)

    def get_queryset(self):
        user = self.request.user
        return Section.objects.filter(corp_id__infrastructure_id__owner=user)

