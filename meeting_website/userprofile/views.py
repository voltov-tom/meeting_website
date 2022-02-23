from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from userprofile.models import CustomUser
from userprofile.serializers import RegistrationSerializer, UserSerializer


class UserListView(CreateAPIView):
    permission_classes = (AllowAny,)

    serializer_class = RegistrationSerializer


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
