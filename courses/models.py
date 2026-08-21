from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True, default="")

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):

    CERTIFICATE_CHOICES = (
        ("USCG", "US Coast Guard"),
        ("FCC", "FCC"),
        ("MARINERS", "Mariners"),
        ("OTHER", "Other"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    course_name = models.CharField(max_length=255)

    short_description = models.CharField(
        max_length=300,
        blank=True
    )

    description = models.TextField()

    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration = models.CharField(max_length=100)

    pass_percentage = models.PositiveIntegerField(default=70)

    certificate_type = models.CharField(
        max_length=20,
        choices=CERTIFICATE_CHOICES,
        default="MARINERS"
    )

    thumbnail = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.course_name

class Module(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules"
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.course_name} - {self.title}"


class Lesson(models.Model):

    CONTENT_TYPE_CHOICES = (
        ("VIDEO", "Video"),
        ("SCREEN", "Screen Recording"),
        ("AUDIO", "Audio"),
        ("TEXT", "Text"),
    )

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    content = models.TextField(blank=True)

    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        default="VIDEO"
    )

    media_url = models.URLField(
    blank=True,
    null=True
    )

    media_file = models.FileField(
        upload_to="lessons/media/",
        blank=True,
        null=True
    )

    resource_file = models.FileField(
        upload_to="lessons/resources/",
        blank=True,
        null=True
    )

    duration = models.CharField(
        max_length=50,
        blank=True
    )

    order = models.PositiveIntegerField(
        default=1
    )

    is_preview = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.module.title} - {self.title}"