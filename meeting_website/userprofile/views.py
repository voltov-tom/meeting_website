from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from userprofile.models import CustomUser, Sympathy
from userprofile.serializers import RegistrationSerializer, UserSerializer, UserLikesSerializer
from userprofile.utils import send_notification


class CreateUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class UserLikesView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Sympathy.objects.all()
    serializer_class = UserLikesSerializer

    def post(self, request, id):
        # add sympathy when 'id' -> 'liked user'
        user = request.user
        try:
            obj = Sympathy.objects.get(user=user)
        except Exception:  # TODO create custom exception
            request.user.sympathy.create()
            obj = Sympathy.objects.get(user=user)

        obj.like.add(id)
        obj.save()

        # check for mutual sympathy and send e-mails if exists
        query = Sympathy.objects.filter(id=id).values('like')
        for i in range(len(query)):
            if user.id in query[i].values():
                user_1 = CustomUser.objects.get(id=request.user.id)
                user_2 = CustomUser.objects.get(id=id)
                send_notification(user_1, user_2)
                break

        return Response(status=status.HTTP_201_CREATED)


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
