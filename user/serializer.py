from rest_framework import serializers
from user.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token


class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user  = super().create(validated_data) # 저장하고
        password = user.password
        user.set_password(password) # 지정하고
        user.save() # 다시 저장?
        return user

