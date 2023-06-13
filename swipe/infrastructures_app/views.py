from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from drf_psq import Rule, PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from infrastructures_app.models import Corp, Section, Infrastructure, Image, Apartment
from infrastructures_app.serializers import *
from user_app.permissions import IsManager, IsManagerOrOwner, IsUser


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


@extend_schema(tags=['Infrastructure'])
class InfrastructureViewSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = InfrastructureSerializer
    queryset = Infrastructure.objects.all()
    http_method_names = ['get', 'put', 'delete']
    parser_classes = [JSONParser]

    psq_rules = {
        ('update', 'destroy'): [
            Rule([AllowAny], InfrastructureUpDelSerializer),
        ],
        ('list', 'retrieve'): [
            Rule([AllowAny], InfrastructureSerializer)
        ]
    }

    @action(methods=['get'], detail=False, url_name='my')
    def my_infrastructure(self, request):
        try:
            instance = Infrastructure.objects.get(owner=self.request.user.id)
            serializer = self.get_serializer(instance, many=False)
            return Response(serializer.data)
        # except ObjectDoesNotExist:
        #     raise APIException('Infrastructure not found', code=404)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Apartment'])
class ApartmentViewSet(PsqMixin, viewsets.ModelViewSet):
    # serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    parser_classes = [MultiPartParser]

    psq_rules = {
        'create': [
            Rule([IsUser], ApartmentCreateSerializer),
        ],
        ('list', 'retrieve'): [
            Rule([AllowAny], ApartmentSerializer),
        ],
        ('update', 'destroy'): [
            Rule([AllowAny], ApartmentUpdateSerializer)
        ],
        ('accept_apart'): [
            Rule([IsManager], AcceptSerializer)
        ]
    }
    @extend_schema(request=ApartmentCreateSerializer, responses=ApartmentCreateSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(self, request, *args, **kwargs)

    @extend_schema(request=ApartmentUpdateSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)

    @action(methods=['get'], detail=False, url_name='my', serializer_class=ApartmentSerializer)
    def my_apartment_list(self, request):
        if not IsUser().has_permission(request, self):
            return Response({'detail': 'Недостаточно прав доступа'}, status=status.HTTP_403_FORBIDDEN)
        queryset = Apartment.objects.filter(infrastructure_id__owner=self.request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['patch'], detail=True, url_name='accept_apart', serializer_class=AcceptSerializer)
    def accept_apart(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Save the updated instance
        return Response(serializer.data)
