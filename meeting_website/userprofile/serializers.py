from django.contrib.gis.geos import Point
from rest_framework.serializers import ModelSerializer

from userprofile.models import CustomUser, Sympathy


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'profile_picture',)


class UserLikesSerializer(ModelSerializer):
    class Meta:
        model = Sympathy
        fields = ('user', 'like')


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password', 'gender', 'profile_picture', 'location',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            validated_data['first_name'],
            validated_data['last_name'],
            validated_data['email'],
            validated_data['password'],
            validated_data['gender'],
            validated_data['profile_picture'],
            Point(tuple(float(i) for i in validated_data['location'].split(','))),  # many moves from str to PointField
        )
        return user
