from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_info_about_update_course(email):
    send_mail(
        "Обновление курса", "Произошло обновление курса", EMAIL_HOST_USER, [email]
    )
