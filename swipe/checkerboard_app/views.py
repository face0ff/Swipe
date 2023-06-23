from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView

from checkerboard_app.models import Checkerboard, Floor, Riser
from checkerboard_app.serializers import CheckerboardSerializer, FloorSerializer, RiserSerializer
from user_app.permissions import IsOwner, IsManagerOrOwner


@extend_schema(tags=['Checkerboard'])
class CheckerboardUpdate(UpdateAPIView):
    queryset = Checkerboard.objects.all()
    serializer_class = CheckerboardSerializer
    http_method_names = ['put']

@extend_schema(tags=['Checkerboard'])
class CheckerboardList(ListAPIView):
    queryset = Checkerboard.objects.all()
    serializer_class = CheckerboardSerializer
    http_method_names = ['get']

@extend_schema(tags=['Floor'])
class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsManagerOrOwner,)


@extend_schema(tags=['Floor'])
class FloorList(ListAPIView):
    serializer_class = FloorSerializer
    http_method_names = ['get']
    permission_classes = (IsManagerOrOwner,)

    def get_queryset(self):
        user = self.request.user
        return Floor.objects.filter(section_id__corp_id__infrastructure_id__owner_id=user)

@extend_schema(tags=['Riser'])
class RiserViewSet(viewsets.ModelViewSet):
    queryset = Riser.objects.all()
    serializer_class = RiserSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsManagerOrOwner,)


@extend_schema(tags=['Riser'])
class RiserList(ListAPIView):
    serializer_class = RiserSerializer
    http_method_names = ['get']
    permission_classes = (IsManagerOrOwner,)

    def get_queryset(self):
        user = self.request.user
        return Riser.objects.filter(section_id__corp_id__infrastructure_id__owner_id=user)
