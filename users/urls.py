
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentListAPIView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "users"

router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns =[
    path('payments/', PaymentListAPIView.as_view(), name='payments_list'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('api/token/', TokenRefreshView.as_view(), name='token_refresh'),
             ] + router.urls