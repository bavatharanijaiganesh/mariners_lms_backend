from django.urls import path
from .views import (
    CreatePaymentIntent,
    PaymentSuccessView,
)


urlpatterns = [
    path(
        "create-payment-intent/",
        CreatePaymentIntent.as_view()
    ),
    path(
        "payment-success/<int:pk>/",
        PaymentSuccessView.as_view()
    ),

]