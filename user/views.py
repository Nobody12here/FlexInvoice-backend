from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializer import UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user: User = serializer.save()
            return Response(
                {
                    "message": "User created sucessfully",
                    "id": user.pk,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
