from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def inactive_users():
    users = CustomUser.objects.filter(is_active=True)

    for user in users:

        if user.last_login is None:
            continue

        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()