from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from .serializers import UserProfileSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Viewset for :model: 'users.CustomUser'
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer