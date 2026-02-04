from tkinter.constants import CASCADE

from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class CustomUser(AbstractUser):
    """
    Custom model for user. Email is used as a username field.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    city = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Город проживания"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """

    """

    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Наличные'
        BANK = 'BANK', 'Банковский перевод'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payment', verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payment', null=True, blank=True,
                                    verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='payment', null=True, blank=True,
                                    verbose_name='Оплаченный урок')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=4, choices=PaymentMethod.choices, verbose_name='Способ оплаты')
