from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsNotModerator, IsModeratorOrOwner, IsOwner


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

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Moderators').exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsNotModerator()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsNotModerator(), IsOwner]
        elif self.action in ['update', 'retrieve']:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        return [IsAuthenticated()]


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

    def get_queryset(self):
        if self.request.user.groups.filter(name='Moderators').exists():
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
