from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("STUDENT", "Student"),
    )

    username = None

    full_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="STUDENT",
    )

    # =========================
    # MARINER PROFILE DETAILS
    # =========================

    cdc_number = models.CharField(
        max_length=50,
        blank=True
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    rank = models.CharField(
        max_length=100,
        blank=True
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    emergency_contact = models.CharField(
        max_length=20,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.full_name