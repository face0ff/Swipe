from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from filters_app.models import Filter
from filters_app.serializers import FilterSerializer
from user_app.permissions import IsUser


# Create your views here.
@extend_schema(tags=['Filters'])
class FiltersViewSet(viewsets.ModelViewSet):
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsUser,)

    def get_queryset(self):
        user = self.request.user
        filter = Filter.objects.filter(user_id=user)
        return filter
