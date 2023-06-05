
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from user_app.views import *


router = routers.SimpleRouter()
router.register(r'notaries', NotariesViewSet)
router.register(r'user_create', UserAdminViewSet)
router.register(r'user_register', UserRegisterViewSet)
router.register(r'owner_register', OwnerRegisterViewSet)
router.register(r'user_list', ManagerUserListViewSet)
router.register(r'message', MessageViewSet)


urlpatterns = [


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),


    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/registration/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api/auth/', include('allauth.urls')),

    path('api/v1/', include(router.urls)),
    path('api/v1/user_update/', UserViewSet.as_view({'put': 'update'}), name='user_update'),
    path('api/v1/owner_update/', OwnerViewSet.as_view({'put': 'update'}), name='owner_update'),
    path('api/v1/user_list/<int:pk>/black_list ', BlackListUpdate.as_view(), name='black_list_update'),
    path('api/v1/message/<int:pk>/user', MessageUserGet.as_view({'get': 'list'}), name='Message'),
    path('api/v1/subscription/', SubscriptionGet.as_view(), name='Subscription'),
    path('api/v1/subscription_create/', SubscriptionCreate.as_view(), name='Subscription'),
    path('api/v1/subscription_update/', SubscriptionUpdate.as_view(), name='Subscription'),



]
