from rest_framework import serializers
from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source="student.full_name",
        read_only=True
    )

    student_email = serializers.CharField(
        source="student.email",
        read_only=True
    )

    class Meta:

        model = Enrollment

        fields = "__all__"

        read_only_fields = (
            "student",
            "status",
            "enrolled_at",
        )


# from rest_framework import serializers
# from .models import Enrollment


# class EnrollmentSerializer(serializers.ModelSerializer):

#     course_name = serializers.CharField(
#         source="course.course_name",
#         read_only=True
#     )

#     class Meta:

#         model = Enrollment

#         fields = "__all__"

#         read_only_fields = (
#             "student",
#             "status",
#             "enrolled_at",
#         )