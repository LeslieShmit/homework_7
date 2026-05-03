from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[LinkValidator()]
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons_detailed = LessonSerializer(source="lessons", many=True)

    class Meta:
        model = Course
        fields = (
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons_detailed",
        )

    def get_lessons_count(self, instance):
        return instance.lessons.count()
