from rest_framework import generics, viewsets

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model: 'materials.Course'
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Creates an object of :model: 'materials.Lesson'
    """

    serializer_class = LessonSerializer

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


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieve the details of a specific object :model: 'materials.Lesson'
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Updates the details of a specific object :model: 'materials.Lesson'
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Deletes the specific object :model: 'materials.Lesson'
    """

    queryset = Lesson.objects.all()
