from django.urls import path
from .views import (EnrollmentListCreateView,  EnrollmentDetailView,  MyCoursesView, StudentCourseLessonsView, StudentCourseContentView)

urlpatterns = [

    path(
        "enrollments/",
        EnrollmentListCreateView.as_view(),
        # name="enrollments",
        name="enrollment-list-create",
    ),
    path(
        "enrollments/<int:pk>/",
        EnrollmentDetailView.as_view(),
        name="enrollment-detail",
    ),

    path(
        "my-courses/",
        MyCoursesView.as_view()
    ),
    path(
        "student/courses/<str:course_id>/lessons/",
        StudentCourseLessonsView.as_view(),
        name="student-course-lessons"
    ),
    path(
        "student/course/<str:course_id>/content/",
        StudentCourseContentView.as_view(),
        name="student-course-content"
    ),

]