"""
URL configuration for swipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from user_app.views import NotariesViewSet, UserViewSet, UserAdminViewSet, OwnerViewSet, UserRegisterViewSet, \
    OwnerRegisterViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.SimpleRouter()
router.register(r'notaries', NotariesViewSet)
router.register(r'user_create', UserAdminViewSet)
router.register(r'user_update', UserViewSet)
router.register(r'owner_update', OwnerViewSet)
router.register(r'user_register', UserRegisterViewSet)
router.register(r'owner_register', OwnerRegisterViewSet)

urlpatterns = [

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),


    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/registration/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api/auth/', include('allauth.urls')),

    path('api/v1/', include(router.urls)),

]
