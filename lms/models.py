from django.db import models
from accounts.models import User
# from lms.models import Enrollment


class Enrollment(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("CANCELLED", "Cancelled"),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    course_id = models.CharField(max_length=50)

    course_name = models.CharField(max_length=255)

    category = models.CharField(max_length=100)

    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration = models.CharField(max_length=100)

    certificate_type = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course_name}"

class LessonAccess(models.Model):
    enrollment = models.ForeignKey(
        "Enrollment",
        on_delete=models.CASCADE
    )

# from django.db import models
# from accounts.models import User
# from courses.models import Course


# class Enrollment(models.Model):

#     STATUS_CHOICES = (
#         ("PENDING", "Pending"),
#         ("PAID", "Paid"),
#         ("CANCELLED", "Cancelled"),
#     )

#     student = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="enrollments"
#     )

#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name="enrollments"
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="PENDING"
#     )

#     enrolled_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     class Meta:
#         unique_together = ("student", "course")

#     def __str__(self):
#         return f"{self.student.full_name} - {self.course.course_name}"