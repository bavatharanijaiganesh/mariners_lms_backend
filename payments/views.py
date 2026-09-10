import stripe

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from lms.models import Enrollment


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntent(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            amount = float(request.data["amount"])
            enrollment_id = request.data.get("enrollment_id")

            enrollment = Enrollment.objects.get(
                id=enrollment_id,
                student=request.user,
                status="PENDING"
            )

            amount_in_cents = int(amount * 100)

            intent = stripe.PaymentIntent.create(

                amount=amount_in_cents,

                currency="usd",

                automatic_payment_methods={
                    "enabled": True
                },

                metadata={
                    "enrollment_id": str(enrollment.id),
                    "student_id": str(request.user.id),
                }
            )

            return Response({
                "clientSecret": intent.client_secret
            })

        except Enrollment.DoesNotExist:

            return Response(
                {
                    "error": "Pending enrollment not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentSuccessView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            payment_intent_id = request.data.get(
                "payment_intent_id"
            )

            if not payment_intent_id:

                return Response(
                    {
                        "error": "Payment Intent ID is required."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get payment details from Stripe
            intent = stripe.PaymentIntent.retrieve(
                payment_intent_id
            )

            # Verify Stripe payment
            if intent.status != "succeeded":

                return Response(
                    {
                        "error": "Payment has not succeeded."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify enrollment belongs to logged-in student
            enrollment = Enrollment.objects.get(
                id=pk,
                student=request.user,
                status="PENDING"
            )

            # Verify this payment belongs to this enrollment
            if intent.metadata.get("enrollment_id") != str(enrollment.id):

                return Response(
                    {
                        "error": "Payment does not belong to this enrollment."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            enrollment.status = "PAID"

            enrollment.save()

            return Response({
                "message": "Payment Successful",
                "enrollment_id": enrollment.id,
                "status": "PAID"
            })

        except Enrollment.DoesNotExist:

            return Response(
                {
                    "error": "Enrollment not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except stripe.error.StripeError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )