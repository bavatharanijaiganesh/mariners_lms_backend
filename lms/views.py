from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from courses.models import Lesson, Module
from lms.models import Enrollment
from courses.serializers import ModuleSerializer


class EnrollmentListCreateView(ListCreateAPIView):

    serializer_class = EnrollmentSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        # Student can see their own enrollments
        # including PENDING and PAID
        if user.role == "STUDENT":

            return Enrollment.objects.filter(
                student=user
            ).order_by("-enrolled_at")

        # Admin can see all enrollments
        return Enrollment.objects.all().order_by(
            "-enrolled_at"
        )

    def perform_create(self, serializer):

        course_id = self.request.data.get("course_id")

        print(
            "Logged in user:",
            self.request.user.email
        )

        print(
            "Received course_id:",
            course_id
        )

        already_exists = Enrollment.objects.filter(
            student=self.request.user,
            course_id=course_id,
            status="PAID"
        ).exists()

        print(
            "Already has PAID enrollment:",
            already_exists
        )

        if already_exists:

            raise ValidationError(
                {
                    "message":
                    "You have already enrolled in this course."
                }
            )

        serializer.save(
            student=self.request.user
        )


class EnrollmentDetailView(
    RetrieveUpdateDestroyAPIView
):
    queryset = Enrollment.objects.all()

    serializer_class = EnrollmentSerializer

    permission_classes = [IsAuthenticated]


class MyCoursesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        enrollments = Enrollment.objects.filter(
            student=request.user,
            status="PAID"
        ).order_by("-enrolled_at")

        serializer = EnrollmentSerializer(
            enrollments,
            many=True
        )

        return Response(serializer.data)

class StudentCourseLessonsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        # Check whether this student has PAID for the course
        enrollment = Enrollment.objects.filter(
            student=request.user,
            course_id=course_id,
            status="PAID"
        ).first()

        if not enrollment:
            return Response(
                {
                    "detail": "Please purchase this course to access lessons."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Get modules belonging to this course
        modules = Module.objects.filter(
            course_id=course_id
        ).order_by("order")

        data = []

        for module in modules:

            lessons = Lesson.objects.filter(
                module=module,
                is_active=True
            ).order_by("order")

            data.append({
                "id": module.id,
                "title": module.title,
                "description": module.description,
                "order": module.order,
                "lessons": [
                    {
                        "id": lesson.id,
                        "title": lesson.title,
                        "description": lesson.description,
                        "content": lesson.content,
                        "content_type": lesson.content_type,
                        "media_url": lesson.media_url,
                        "resource_file": (
                            request.build_absolute_uri(
                                lesson.resource_file.url
                            )
                            if lesson.resource_file
                            else None
                        ),
                        "duration": lesson.duration,
                        "order": lesson.order,
                        "is_preview": lesson.is_preview,
                    }
                    for lesson in lessons
                ]
            })

        return Response(data)

class StudentCourseContentView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        # Check whether this logged-in student has PAID
        enrollment = Enrollment.objects.filter(
            student=request.user,
            course_id=course_id,
            status="PAID"
        ).first()

        if not enrollment:
            return Response(
                {
                    "detail": "Please purchase this course."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Get modules belonging to the course
        modules = Module.objects.filter(
            course_id=course_id
        ).order_by("order")

        serializer = ModuleSerializer(
            modules,
            many=True
        )

        return Response(
            {
                "course_id": course_id,
                "status": "PAID",
                "modules": serializer.data
            }
        )



