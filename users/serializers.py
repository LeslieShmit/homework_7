from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Payment

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
        )
        read_only_fields = ('id',)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ='__all__'