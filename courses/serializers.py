from rest_framework import serializers
from .models import Category, Course, Module, Lesson


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


# class CourseSerializer(serializers.ModelSerializer):

#     category_name = serializers.CharField(
#         source="category.name",
#         read_only=True
#     )

#     class Meta:
#         model = Course
#         fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:

        model = Course
        fields = "__all__"

        # fields = [
        #     "id",
        #     "course_name",
        #     "category",
        #     "category_name",
        #     "fee",
        #     "estimated_duration",
        #     "description",
        #     "thumbnail",
        #     "pass_percentage",
        #     "certificate_type",
        #     "is_active",
        #     "created_at",
        #     "updated_at",
        # ]
# class ModuleSerializer(serializers.ModelSerializer):

#     course_name = serializers.CharField(
#         source="course.course_name",
#         read_only=True
#     )

#     class Meta:

#         model = Module

#         fields = "__all__"


# class ModuleSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Module
#         fields = "__all__"

# class LessonSerializer(serializers.ModelSerializer):

#     module_title = serializers.CharField(
#         source="module.title",
#         read_only=True
#     )

#     class Meta:
#         model = Lesson
#         fields = "__all__"   


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
            "created_at",
            "updated_at",
        ]


class ModuleSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            "id",
            "course_id",
            "title",
            "description",
            "order",
            "created_at",
            "lessons",
        ]          