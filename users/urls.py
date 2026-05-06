from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (MyTokenObtainPairView, PaymentCreateApiView,
                    PaymentListAPIView, PaymentUpdateApiView, UserViewSet)

app_name = "users"

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payment/create/", PaymentCreateApiView.as_view(), name="payment"),
    path(
        "payment/<int:pk>/update/",
        PaymentUpdateApiView.as_view(),
        name="payment_update",
    ),
    path(
        "login/",
        MyTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "api/token/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
] + router.urls
