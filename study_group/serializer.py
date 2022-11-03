from rest_framework import serializers
from study_group.models import Study, Student

class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model=Study
        fields='__all__'


# 리스트
class StudyListSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    like_count=serializers.SerializerMethodField()
    student_count=serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    def get_like_count(self, obj):
        return obj.like.count()
    def get_student_count(self, obj): # 여기서 obj로 스터디 객체 가져온거다 obj.id사용해도 된다 
        return obj.student_set.filter(id=obj.id, is_accept=True).count()     # 스터디를 바라보는 걸 다 가져왔다 여기서 필터를 건다 가능
    
    class Meta:
        model=Study
        fields=("student_count", "title","content","thumbnail_img","headcount","user","like_count","create_dt")



class StudyDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model=Study
        fields='__all__'