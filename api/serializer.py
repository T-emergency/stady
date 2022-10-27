from rest_framework import serializers

from study.models import StudyLog
from study_group.models import Study, Student



class StudySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Study
        fields = ["id", "user", "create_dt", "content", "on_off_line", "headcount"]

# 다른 방법은 없는지 찾아보고 & 여쭤보기 # 이방법은 데이터 베이스를 많이 참조하지 않나라는 생각?
class StudyDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    is_like = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    is_student = serializers.SerializerMethodField()
    sended = serializers.SerializerMethodField()
    thumbnail_img = serializers.SerializerMethodField()

    def get_is_like(self, obj):
        flag = obj.like.filter(id = self.context.get('request').user.id).exists()
        return flag

    def get_is_author(self, obj):
        flag = False
        if obj.user == self.context.get('request').user:
            flag = True
        return flag

    def get_is_student(self, obj):
        flag = obj.student_set.filter(user = self.context.get('request').user, post = obj, is_accept = True).exists()
        return flag

    def get_sended(self, obj):
        flag = obj.student_set.filter(user = self.context.get('request').user, post = obj, is_accept = None).exists()
        return flag

    def get_thumbnail_img(self, obj):
        return obj.thumbnail_img.url

    class Meta:
        model = Study
        fields = ['id', 'user','headcount', 'content','on_off_line', 'is_like', 'thumbnail_img','is_author', 'is_student', 'sended']