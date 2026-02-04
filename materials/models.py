from django.db import models

class Lesson(models.Model):
    """
    Stores a single lesson.
    """
    title = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="previews/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    video_link = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Course(models.Model):
    """
    Stores a single course, which is a group of lessons in fact. Related to :model: 'materials.Lesson'.
    """
    title = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="previews/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    lessons = models.ManyToManyField(Lesson, null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"