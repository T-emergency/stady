from rest_framework import serializers
from user.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token





# class UserFollowSerializer(serializers.ModelSerializer):
#     email = serializers.StringRelatedField()
#     class Meta:
#         model = User
#         fields = ['email','id']


# class UserSerializer(serializers.ModelSerializer):
#     # followings = UserFollowSerializer(many = True)
#     followings = serializers.StringRelatedField(many = True)

#     class Meta:
#         model = User
#         fields = '__all__'

#     def create(self, validated_data):
#         user  = super().create(validated_data) # 저장하고
#         password = user.password
#         user.set_password(password) # 지정하고
#         user.save() # 다시 저장?
#         return user

#     # def update(self, vaildated_data): #비밀번호 변경을 따로 만들어서 회원의 일부를 수정가능하게 만드는 법 알기


# class UserProfileSerializer(serializers.ModelSerializer):

#     article_set = ArticleSerializer(many = True)
#     following_count = serializers.SerializerMethodField()
#     follower_count = serializers.SerializerMethodField()
#     article_like = serializers.StringRelatedField(many = True)

#     def get_follower_count(self, obj):
#         return obj.followers.count()

#     def get_following_count(self, obj):
#         return obj.followings.count()

#     class Meta:
#         model = User
#         fields = '__all__'
