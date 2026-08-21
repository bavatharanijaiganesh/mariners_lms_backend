# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Category, Course, Module,Lesson
from .serializers import CategorySerializer, CourseSerializer, ModuleSerializer, LessonSerializer

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all().order_by("id")

    serializer_class = CategorySerializer
    parser_classes = [MultiPartParser, FormParser]


class CourseListCreateView(ListCreateAPIView):

    queryset = Course.objects.all().order_by("-created_at")

    serializer_class = CourseSerializer


class CourseDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Course.objects.all()

    serializer_class = CourseSerializer    

# class CategoryListView(generics.ListAPIView):

#     queryset = Category.objects.filter(is_active=True)

#     serializer_class = CategorySerializer

# class CategoryCreateView(generics.CreateAPIView):

#     queryset = Category.objects.all()

#     serializer_class = CategorySerializer

#     permission_classes = [IsAuthenticated]

# class CourseListView(generics.ListAPIView):

#     queryset = Course.objects.filter(is_active=True)

#     serializer_class = CourseSerializer

# class CourseCreateView(generics.CreateAPIView):

#     queryset = Course.objects.all()

#     serializer_class = CourseSerializer

#     permission_classes = [IsAuthenticated]    

# class ModuleListCreateView(ListCreateAPIView):

#     queryset = Module.objects.all().order_by("order")

#     serializer_class = ModuleSerializer

#     permission_classes = [IsAuthenticated]


class ModuleListCreateView(ListCreateAPIView):

    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        course_id = self.request.query_params.get("course_id")

        if course_id:
            return Module.objects.filter(
                course_id=course_id
            ).order_by("order")

        return Module.objects.all().order_by("order")

class ModuleDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Module.objects.all()

    serializer_class = ModuleSerializer

    permission_classes = [IsAuthenticated]


# class LessonListCreateView(ListCreateAPIView):

#     queryset = Lesson.objects.all().order_by("order")

#     serializer_class = LessonSerializer

#     permission_classes = [IsAuthenticated]

# class LessonListCreateView(ListCreateAPIView):

#     serializer_class = LessonSerializer

#     permission_classes = [IsAuthenticated]

#     parser_classes = [MultiPartParser, FormParser]

#     def get_queryset(self):

#         module_id = self.request.query_params.get("module")

#         if module_id:
#             return Lesson.objects.filter(
#                 module_id=module_id
#             ).order_by("order")

#         return Lesson.objects.all().order_by("order")


# class LessonListCreateView(ListCreateAPIView):

#     serializer_class = LessonSerializer

#     permission_classes = [IsAuthenticated]

#     parser_classes = [MultiPartParser, FormParser]

#     def get_queryset(self):

#         module_id = self.request.query_params.get("module")

#         # No module specified
#         if not module_id:
#             return Lesson.objects.none()

#         # Get the module
#         try:
#             module = Module.objects.get(id=module_id)
#         except Module.DoesNotExist:
#             return Lesson.objects.none()

#         # Course ID from Module
#         course_id = module.course_id

#         # Check whether logged-in student has PAID
#         has_access = Enrollment.objects.filter(
#             student=self.request.user,
#             course_id=course_id,
#             status="PAID"
#         ).exists()

#         if not has_access:
#             from rest_framework.exceptions import PermissionDenied

#             raise PermissionDenied(
#                 "Please purchase this course to access the lessons."
#             )

#         # User has paid
#         return Lesson.objects.filter(
#             module_id=module_id
#         ).order_by("order")

class LessonListCreateView(ListCreateAPIView):

    serializer_class = LessonSerializer

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):

        module_id = self.request.query_params.get("module")

        if not module_id:
            return Lesson.objects.none()

        # ADMIN can access all lessons
        if self.request.user.role == "ADMIN":
            return Lesson.objects.filter(
                module_id=module_id
            ).order_by("order")

        # STUDENT
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Lesson.objects.none()

        course_id = module.course_id

        has_access = Enrollment.objects.filter(
            student=self.request.user,
            course_id=course_id,
            status="PAID"
        ).exists()

        if not has_access:
            raise PermissionDenied(
                "Please purchase this course to access the lessons."
            )

        return Lesson.objects.filter(
            module_id=module_id
        ).order_by("order")

# class LessonDetailView(RetrieveUpdateDestroyAPIView):

#     queryset = Lesson.objects.all()

#     serializer_class = LessonSerializer

#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

class LessonDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = LessonSerializer

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):

        return Lesson.objects.filter(
            module__course_id__in=Enrollment.objects.filter(
                student=self.request.user,
                status="PAID"
            ).values("course_id")
        )
