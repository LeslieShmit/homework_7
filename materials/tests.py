from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import CustomUser


class TestCourseLesson(APITestCase):
    """Тест курса и урока."""

    def setUp(self) -> None:
        """Создание тестового пользователя для авторизации."""

        self.user = CustomUser.objects.create(email="test@test.com")
        self.user.set_password("password123")
        self.user.save()

        self.course = Course.objects.create(
            title="Test_Course_1", description="Test_Course_1", owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title="Test_Lesson_1",
            description="Test_Lesson_1",
            owner=self.user,
        )

        self.course.lessons.add(self.lesson)

        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """Тест создание курса."""

        data = {
            "title": "Test_course_2",
            "description": "Test_course_2",
        }

        response = self.client.post("/materials/courses/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_course = Course.objects.get(pk=response.data["id"])

        self.assertEqual(created_course.title, "Test_course_2")
        self.assertEqual(created_course.description, "Test_course_2")
        self.assertEqual(created_course.owner, self.user)

    def test_create_lesson(self):
        """Тест создания урока."""

        data = {
            "title": "New_lesson",
            "description": "New_lesson",
        }

        response = self.client.post("/materials/lesson/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        lesson_id = response.data["id"]
        created_lesson = Lesson.objects.get(pk=lesson_id)

        self.assertEqual(created_lesson.title, "New_lesson")
        self.assertEqual(created_lesson.description, "New_lesson")
        self.assertEqual(created_lesson.owner, self.user)

        self.course.lessons.add(created_lesson)

        self.assertIn(created_lesson, self.course.lessons.all())

    def test_update_lesson(self):
        """Тест обновление урока."""

        updated_data = {
            "title": "Updated_test_lesson",
            "description": "Updated_test_description",
        }

        response = self.client.patch(
            f"/materials/lesson/{self.lesson.id}/edit/", data=updated_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_lesson = Lesson.objects.get(id=self.lesson.id)

        self.assertEqual(updated_lesson.title, "Updated_test_lesson")
        self.assertEqual(updated_lesson.description, "Updated_test_description")

        self.assertIn(updated_lesson, self.course.lessons.all())

    def test_delete_lesson(self):
        """Тест удаления урока."""

        response = self.client.delete(f"/materials/lesson/{self.lesson.id}/delete/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=self.lesson.id)

    def test_subscribe_toggle(self):
        """Тест подписки/отписки."""

        response = self.client.post(
            "/materials/subscribe/", {"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post(
            "/materials/subscribe/", {"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
