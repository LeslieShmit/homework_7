from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from django_filters import rest_framework as filters

from .models import Payment
from .serializers import UserProfileSerializer, PaymentSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Viewset for :model: 'users.CustomUser'
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    ordering_filter = ('payment_date',)