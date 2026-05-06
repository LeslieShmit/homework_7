from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Payment
from .serializers import (
    MyTokenObtainPairSerializer,
    PaymentSerializer,
    UserProfileSerializer,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Viewset for :model: 'users.CustomUser'
    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_filter = ("payment_date",)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
