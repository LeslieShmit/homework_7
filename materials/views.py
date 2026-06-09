from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorOrOwner, IsNotModerator, IsOwner
from .tasks import send_info_about_update_course


class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model: 'materials.Course'
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Moderators").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsNotModerator()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsNotModerator(), IsOwner]
        elif self.action in ["update", "retrieve"]:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        course = serializer.save()

        subscriptions = Subscription.objects.filter(course=course)

        for subscription in subscriptions:
            send_info_about_update_course.delay(subscription.user.email)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Creates an object of :model: 'materials.Lesson'
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    Retrieve the list of objects :model: 'materials.Lesson'
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieve the details of a specific object :model: 'materials.Lesson'
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Updates the details of a specific object :model: 'materials.Lesson'
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Deletes the specific object :model: 'materials.Lesson'
    """

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator, IsOwner]


class SubscribeView(APIView):
    """Adding or deleting the subscription"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "course_id is required"}, status=400)
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
