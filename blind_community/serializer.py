from rest_framework import serializers
from .models import Post,RandomName,PostComment


class BlindPostSerialize(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude =("user",)


class RandomNameSerialize(serializers.ModelSerializer):
    class Meta:
        model = RandomName
        fields = "__all__"


class BlindPostListView(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     user = obj.user_id
    #     post = obj.id
        
    #     name = RandomName.objects.filter(post=post, user=user)
    #     return name

    random_post= RandomNameSerialize(many=True)
    class Meta:
        model = Post
        fields ="__all__"


class BlindPostDetailSerialize(serializers.ModelSerializer):
    random_post= RandomNameSerialize(many=True)
    class Meta:
        model = Post
        fields = "__all__"


class BlindCommentPostSerialize(serializers.ModelSerializer):
    class Meta:
        model= PostComment
        fields = ("content","post", "user")

