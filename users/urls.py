from tkinter.font import names

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentListAPIView

app_name = "users"

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns =[
    path('payments/', PaymentListAPIView.as_view(), name='payments_list')
             ] + router.urls