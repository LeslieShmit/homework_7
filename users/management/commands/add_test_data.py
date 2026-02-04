from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from materials.models import Lesson, Course
from users.models import Payment


class Command(BaseCommand):
    """
    Custom command to create test data
    WARNING! Use create_admin command before adding test data!
    """

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email="test@sky.pro",
            first_name="John",
            last_name="Doe",
        )

        user.set_password("1234")
        user.is_staff = False
        user.is_superuser = False
        user.save()
        lesson_1 = Lesson.objects.create(title='Test_1')
        lesson_2 = Lesson.objects.create(title='Test_2')
        course = Course.objects.create(title='Test_course',)
        course.lessons.set([lesson_1, lesson_2])
        Payment.objects.create(
            user=user,
            paid_course=course,
            payment_amount=10000.00,
            payment_method='CASH'
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Test data was successfully created."
            )
        )
