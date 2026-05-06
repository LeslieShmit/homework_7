from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Payment
from .serializers import (MyTokenObtainPairSerializer, PaymentSerializer,
                          UserProfileSerializer)
from .services import create_stripe_price, create_stripe_session

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
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_filter = ("payment_date",)

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class PaymentCreateApiView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.paid_lesson:
            title = payment.paid_lesson.title
        else:
            title = payment.paid_course.title

        price = create_stripe_price(payment.payment_amount, title)

        session_id, payment_link = create_stripe_session(price)

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentUpdateApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
