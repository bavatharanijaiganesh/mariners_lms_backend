from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer
from .serializers import LoginSerializer
from .serializers import ProfileSerializer


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "status": True,
                    "message": "Registration Successful",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            data = serializer.validated_data

            return Response(
                {
                    "status": True,
                    "message": "Login Successful",
                    "access": data["access"],
                    "refresh": data["refresh"],
                   "user": {
    "id": data["user"].id,
    "full_name": data["user"].full_name,
    "email": data["user"].email,
    "phone_number": data["user"].phone_number,
    "role": data["user"].role,
    "cdc_number": data["user"].cdc_number,
    "department": data["user"].department,
    "rank": data["user"].rank,
    "location": data["user"].location,
    "emergency_contact": data["user"].emergency_contact,
    "bio": data["user"].bio,
},
                }
            )

        return Response(
            {
                "status": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    # GET PROFILE
    def get(self, request):

        serializer = ProfileSerializer(request.user)

        return Response(
            {
                "status": True,
                "data": serializer.data,
            }
        )

    # UPDATE PROFILE
    class ProfileView(APIView):

        permission_classes = [IsAuthenticated]

    # GET PROFILE
    def get(self, request):

        serializer = ProfileSerializer(request.user)

        return Response(
            {
                "status": True,
                "data": serializer.data,
            }
        )

    # UPDATE PROFILE
    def patch(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "status": True,
                    "message": "Profile updated successfully",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "status": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )