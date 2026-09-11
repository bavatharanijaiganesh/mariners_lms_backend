from rest_framework import serializers
from .models import Category, Course, Module, Lesson


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):

    module_title = serializers.CharField(
        source="module.title",
        read_only=True
    )

    class Meta:
        model = Lesson
        fields = [
            "id",
            "module",
            "module_title",
            "title",
            "description",
            "content",
            "content_type",
            "media_url",
            "media_file",
            "resource_file",
            "duration",
            "order",
            "is_preview",
            "is_active",
        ]


class ModuleSerializer(serializers.ModelSerializer):

    # Frontend can continue sending:
    # { "course_id": 1 }

    course_id = serializers.PrimaryKeyRelatedField(
        source="course",
        queryset=Course.objects.all()
    )

    lessons = LessonSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Module
        fields = [
            "id",
            "course_id",
            "title",
            "description",
            "order",
            "lessons",
        ]