import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lms.models import Enrollment

class CreatePaymentIntent(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        amount = int(float(request.data["amount"]) * 100)

        intent = stripe.PaymentIntent.create(

            amount=amount,

            currency="usd",

            automatic_payment_methods={
                "enabled": True
            }

        )

        return Response({

            "clientSecret": intent.client_secret

        })

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.models import Enrollment


class PaymentSuccessView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        enrollment = Enrollment.objects.get(
            id=pk,
            student=request.user
        )

        enrollment.status = "PAID"

        enrollment.save()

        return Response({
            "message": "Payment Successful"
        })
