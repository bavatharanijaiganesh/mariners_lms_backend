
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [

    path("admin/", admin.site.urls),

    path(
        "api/accounts/",
        include("accounts.urls")
    ),

    path(
        "api/categories/",
        include("courses.category_urls")
    ),

    path(
        "api/courses/",
        include("courses.urls")
    ),

    path(
        "api/payments/",
        include("payments.urls")
    ),

    path(
        "api/lms/",
        include("lms.urls")
    ),

    path(
        "api/exams/",
        include("exams.urls")
    ),

    path(
        "api/certificates/",
        include("certificates.urls")
    ),

    path(
        "api/notifications/",
        include("notifications.urls")
    ),

    path(
        "api/reports/",
        include("reports.urls")
    ),

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

