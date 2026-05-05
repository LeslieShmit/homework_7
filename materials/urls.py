from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView,
                    LessonListAPIView, LessonRetrieveAPIView,
                    LessonUpdateAPIView, SubscribeView)

app_name = "materials"

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_get"),
    path("lesson/<int:pk>/edit/", LessonUpdateAPIView.as_view(), name="lesson_edit"),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete",
    ),path("subscribe/", SubscribeView.as_view(), name="subscribe"),
] + router.urls
