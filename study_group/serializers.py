from rest_framework import serializers

from study_group.models import Study, Student, Tag


# class StudySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Study
#         fields = ["id", "user", "title", "content", "is_online",
#                   "now_cnt", "headcount", "thumbnail_img", "tags"]

#     user = serializers.SerializerMethodField()
#     tags = serializers.SerializerMethodField()  # readonly fields
#     now_cnt = serializers.SerializerMethodField()

#     def get_user(self, obj):
#         return obj.user.username

#     def get_tags(self, obj):
#         return [tag.tag_name for tag in obj.tags.all()]

#     def get_now_cnt(self, obj):
#         return obj.student_set.filter(is_accept=True).count() + 1

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
# # 리스트


# class StudyListSerializer(serializers.ModelSerializer):
#     # user = serializers.SerializerMethodField()
#     like_count = serializers.SerializerMethodField()
#     student_count = serializers.SerializerMethodField()
#     tags = serializers.SerializerMethodField()

#     # def get_user(self, obj):
#     #     print(obj.user)
#     #     user = obj.user.username
#     #     print("user:", user)
#     #     return user

#     def get_like_count(self, obj):
#         return obj.like.count()

#     def get_student_count(self, obj):  # 여기서 obj로 스터디 객체 가져온거다 obj.id사용해도 된다
#         # 스터디를 바라보는 걸 다 가져왔다 여기서 필터를 건다 가능
#         return obj.student_set.filter(id=obj.id, is_accept=True).count()

#     def get_tags(self, obj):
#         return [tag.tag_name for tag in obj.tags.all()]

#     class Meta:
#         model = Study
#         fields = ("id", "student_count", "title", "content", "thumbnail_img",
#                   "headcount", "user", "like_count", "create_dt", "tags")


# # 게시글 작성자 or 참여자
# class StudyAuthorSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()  # 유저
#     # user = serializers.StringRelatedField()
#     is_like = serializers.SerializerMethodField()  # 좋아요
#     is_author = serializers.SerializerMethodField()  # 작성자여부
#     is_student = serializers.SerializerMethodField()  # 참여자
#     thumbnail_img = serializers.SerializerMethodField()  # 썸네일
#     now_cnt = serializers.SerializerMethodField()  # 모집인원
#     sended = serializers.SerializerMethodField()  # 신청자
#     # student_list = serializers.SerializerMethodField() # 신청자 리스트
#     submit = serializers.SerializerMethodField()  # 신청자 리스트
#     tags = serializers.SerializerMethodField()

#     def get_user(self, obj):
#         user = obj.user.username
#         print("get_user: ", user)
#         return user

#     def get_is_like(self, obj):
#         is_like = obj.like.filter(
#             id=self.context.get('request').user.id).exists()
#         return is_like

#     def get_is_author(self, obj):
#         is_author = False
#         if self.context.get('request').user == obj.user:
#             is_author = True
#         return is_author

#     def get_is_student(self, obj):
#         is_student = obj.student_set.filter(user=self.context.get(
#             'request').user, post=obj, is_accept=None).exists()
#         print("참여자: ", is_student)
#         return is_student

#     def get_thumbnail_img(self, obj):
#         thumbnail_img = obj.thumbnail_img
#         return thumbnail_img.url

#     def get_sended(self, obj):
#         sended = obj.student_set.filter(user=self.context.get(
#             'request').user, post=obj, is_accept=True).exists()
#         print("신청자:", sended)
#         return sended

#     def get_now_cnt(self, obj):
#         now_cnt = obj.student_set.filter(post=obj, is_accept=True).count()+1
#         print("신청인원: ", now_cnt)
#         return now_cnt

#     def get_submit(self, obj):
#         if self.get_is_author(obj):
#             submit = [{"id": submit.id, "user": submit.user.username,
#                        "is_accept": submit.is_accept, } for submit in obj.submit.order_by()]
#             # print("dir:",dir(obj.submit))
#             # print("submit:",obj.submit.order_by())
#             print("submit:", submit)
#         else:
#             submit_data = obj.submit.filter(
#                 user=self.context.get('request').user)
#             submit = [{"id": submit.id, "user": submit.user.username,
#                        "is_accept": submit.is_accept, } for submit in submit_data]
#             print(self.context.get('user'))
#             print(submit_data)

#         return submit

#     def get_tags(self, obj):
#         return [tag.tag_name for tag in obj.tags.all()]

#     class Meta:
#         model = Study
#         fields = '__all__'
#         read_only_fields = ['tags', ]


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user.username
        return user

    def get_post(self, obj):
        post = obj.post.id
        return post

    def get_user_id(self, obj):
        user_id = obj.user.id
        return user_id

    class Meta:
        model = Student
        fields = '__all__'


# class TagSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Tag
#         fileds = ['name', ]


class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "user", "title", "content", "is_online",
                  "now_cnt", "headcount", "thumbnail_img", "tags"]

    user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()  # readonly fields
    now_cnt = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    def get_now_cnt(self, obj):
        return obj.student_set.filter(is_accept=True).count() + 1

    def create(self, validated_data):
        validated_data['tags'] = self.context['tags']

        instance = super().create(validated_data)
        return instance


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fileds = ['name', ]

# 다른 방법은 없는지 찾아보고 & 여쭤보기 # 이방법은 데이터 베이스를 많이 참조하지 않나라는 생각?


class StudyDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    is_student = serializers.SerializerMethodField()
    sended = serializers.SerializerMethodField()
    thumbnail_img = serializers.SerializerMethodField()
    now_cnt = serializers.SerializerMethodField()
    # tags = TagSerializer(read_only = True, many = True)
    tags = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_is_like(self, obj):
        flag = obj.like.filter(id=self.context.get('request').user.id).exists()
        return flag

    def get_is_author(self, obj):
        flag = False
        if obj.user == self.context.get('request').user:
            flag = True
        return flag

    def get_is_student(self, obj):
        flag = obj.student_set.filter(user=self.context.get(
            'request').user, post=obj, is_accept=True).exists()
        return flag

    def get_sended(self, obj):
        flag = obj.student_set.filter(user=self.context.get(
            'request').user, post=obj, is_accept=None).exists()
        return flag

    def get_thumbnail_img(self, obj):
        return obj.thumbnail_img.url

    def get_now_cnt(self, obj):
        return obj.student_set.filter(is_accept=True).count() + 1

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    class Meta:
        model = Study
        fields = ['id', 'user', 'headcount', 'title', 'content', 'is_online', 'is_like',
                  'thumbnail_img', 'is_author', 'is_student', 'sended', 'now_cnt', 'tags']
        read_only_fields = ['tags', ]
