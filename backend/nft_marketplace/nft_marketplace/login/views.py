from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token as AuthToken


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user=user)
        return Response({
          "user": UserSerializer(
            user,
            context=self.get_serializer_context()
          ).data,
          "token": token.key
        })


class UserView(generics.RetrieveAPIView):
    permission_classes = [
      permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user
