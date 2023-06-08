
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from checkerboard_app.views import CheckerboardList, CheckerboardUpdate, FloorViewSet, FloorList
from filters_app.views import FiltersViewSet
from infrastructures_app.views import CorpViewSet, CorpCreate, SectionViewSet, CorpList, SectionList
from promotion_app.views import *
from user_app.views import *


router = routers.SimpleRouter()
router.register(r'notaries', NotariesViewSet)
router.register(r'user_create', UserAdminViewSet)
router.register(r'user_register', UserRegisterViewSet)
router.register(r'owner_register', OwnerRegisterViewSet)
router.register(r'user_list', ManagerUserListViewSet)
router.register(r'message', MessageViewSet)
router.register(r'filter', FiltersViewSet)
router.register(r'floor', FloorViewSet)
router.register(r'corp', CorpViewSet)
router.register(r'section', SectionViewSet)


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

    path('api/v1/user_list/<int:pk>/is_block ', BlackListUpdate.as_view(), name='black_list_update'),
    path('api/v1/user_list/user_requests ', UserRequestList.as_view(), name='user_requests'),

    path('api/v1/message/<int:pk>/user', MessageUserGet.as_view({'get': 'list'}), name='Message'),

    path('api/v1/subscription/', SubscriptionGet.as_view(), name='Subscription'),
    path('api/v1/subscription_create/', SubscriptionCreate.as_view(), name='Subscription'),
    path('api/v1/subscription_update/', SubscriptionUpdate.as_view(), name='Subscription'),

    path('api/v1/promotion_update/<int:pk>/', PromotionUpdate.as_view(), name='promotion_update'),
    path('api/v1/promotion_default/<int:pk>/', PromotionDelete.as_view(), name='promotion_default'),

    path('api/v1/checkerboard_get/<int:pk>/', CheckerboardList.as_view(), name='checkerboard_get'),
    path('api/v1/checkerboard_update/<int:pk>/', CheckerboardUpdate.as_view(), name='checkerboard_update'),

    path('api/v1/corp/create', CorpCreate.as_view(), name='corp_create'),
    path('api/v1/corp/list', CorpList.as_view(), name='corp_list'),

    path('api/v1/section/list', SectionList.as_view(), name='section_list'),

    path('api/v1/floor/list', FloorList.as_view(), name='floor_list'),




]
