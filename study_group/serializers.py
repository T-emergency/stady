from rest_framework import serializers

from study_group.models import Study, Student, Tag


# class StudySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Study
#         fields = '__all__'
#         # fields = ('user','create_dt','title','content','thumbnail_img','is_online','headcount')

# # 게시글 작성


# class StudyCreateSerializer(serializers.ModelSerializer):
#     tags = serializers.SerializerMethodField()

#     def get_tags(self, obj):
#         content = self.context.get("request").data.get('tags')
#         return content

#     def create(self, validated_data):
#         content = self.context.get("request").data.get('tags')
#         tags_list = []
#         if content != None:
#             tag_list = content.split(' ')
#             for i in tag_list:
#                 if '#' in i:
#                     tag, _ = Tag.objects.get_or_create(tag_name=i)
#                     tags_list.append(tag.id)
#                 else:
#                     pass
#         validated_data['tags'] = tags_list
#         print(validated_data)

#         instance = super().create(validated_data)
#         return instance

#     class Meta:
#         model = Study
#         fields = ('title', 'content', 'is_online', 'headcount', 'tags')
class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "user","title", "content", "is_online", "headcount", "thumbnail_img", "tags"]

    user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField() # readonly fields

    def get_user(self, obj):
        return obj.user.username

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]
        

    def create(self, validated_data):
        content = self.context.get("request").data.get('tags')
        tags_list = []
        if content != None:
            tag_list = content.split(' ')
            for i in tag_list:
                if '#' in i:
                    tag, _ = Tag.objects.get_or_create(tag_name=i)
                    tags_list.append(tag.id)
                else:
                    pass
        validated_data['tags'] = tags_list
        print(validated_data)

        instance = super().create(validated_data)
        return instance
# 리스트


class StudyListSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     print(obj.user)
    #     user = obj.user.username
    #     print("user:", user)
    #     return user

    def get_like_count(self, obj):
        return obj.like.count()

    def get_student_count(self, obj):  # 여기서 obj로 스터디 객체 가져온거다 obj.id사용해도 된다
        # 스터디를 바라보는 걸 다 가져왔다 여기서 필터를 건다 가능
        return obj.student_set.filter(id=obj.id, is_accept=True).count()

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    class Meta:
        model = Study
        fields = ("student_count", "title", "content", "thumbnail_img",
                  "headcount", "user", "like_count", "create_dt", "tags")


# 게시글 작성자 or 참여자
class StudyAuthorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # 유저
    # user = serializers.StringRelatedField()
    is_like = serializers.SerializerMethodField()  # 좋아요
    is_author = serializers.SerializerMethodField()  # 작성자여부
    is_student = serializers.SerializerMethodField()  # 참여자
    thumbnail_img = serializers.SerializerMethodField()  # 썸네일
    now_cnt = serializers.SerializerMethodField()  # 모집인원
    sended = serializers.SerializerMethodField()  # 신청자
    # student_list = serializers.SerializerMethodField() # 신청자 리스트
    submit = serializers.SerializerMethodField()  # 신청자 리스트

    def get_user(self, obj):
        user = obj.user.username
        print("get_user: ", user)
        return user

    def get_is_like(self, obj):
        is_like = obj.like.filter(id=self.context.get('user').id).exists()
        return is_like

    def get_is_author(self, obj):
        is_author = False
        if self.context.get('user') == obj.user:
            is_author = True
        return is_author

    def get_is_student(self, obj):
        is_student = obj.student_set.filter(user=self.context.get(
            'user'), post=obj, is_accept=None).exists()
        print("참여자: ", is_student)
        return is_student

    def get_thumbnail_img(self, obj):
        thumbnail_img = obj.thumbnail_img
        return thumbnail_img.url

    def get_sended(self, obj):
        sended = obj.student_set.filter(user=self.context.get(
            'user'), post=obj, is_accept=True).exists()
        print("신청자:", sended)
        return sended

    def get_now_cnt(self, obj):
        now_cnt = obj.student_set.filter(post=obj, is_accept=True).count()+1
        print("신청인원: ", now_cnt)
        return now_cnt

    # def get_student_list(self, obj):
    #     student_list = [student.user.username for student in obj.student_set.filter(post=obj)]
    #     # print(dir(student_list))
    #     # print(student_list)
    #     return student_list

    def get_submit(self, obj):
        if self.get_is_author(obj):
            submit = [{"id": submit.id, "user": submit.user.username,
                       "is_accept": submit.is_accept, } for submit in obj.submit.order_by()]
            # print("dir:",dir(obj.submit))
            # print("submit:",obj.submit.order_by())
            print("submit:", submit)
        else:
            submit_data = obj.submit.filter(user=self.context.get('user'))
            submit = [{"id": submit.id, "user": submit.user.username,
                       "is_accept": submit.is_accept, } for submit in submit_data]
            print(self.context.get('user'))
            print(submit_data)

        return submit

    class Meta:
        model = Study
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user.username
        return user

    def get_post(self, obj):
        post = obj.post.id
        return post

    class Meta:
        model = Student
        fields = '__all__'
