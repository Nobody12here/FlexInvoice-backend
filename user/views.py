from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializer import UserSerializer
from common.utils import CommonUtils

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


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Email Field"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Password"
                ),
            },
            required=["email", "password"],
        )
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                # generate jwt token for this user
                access_tokens = CommonUtils().create_access(user)
                return Response(
                    {"message": "Login sucessfully!","data":access_tokens}, status=status.HTTP_200_OK
                )
        except User.DoesNotExist:
            pass
        return Response(
            {
                "error": "Incorrect email or password try again!",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
