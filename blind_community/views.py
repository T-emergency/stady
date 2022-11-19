from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializer import BlindPostSerialize,BlindPostListView,BlindPostDetailSerialize,BlindCommentPostSerialize
from .models import RandomName, Post,PostComment,Like
import random

first = ['케케묵은', '질긴', '짖궂은', '엄청난', '옳은', '외로운', '나쁜', '그리운', '날카로운', '네모난','열받은','잠오는'] 
second = ['우유','연필','컵','커피','사과','고양이','강아지','물망초','냉장고','가방','서랍','책상']

class BlindPostView(APIView):
    def post(self, request, category):
        if category == 'blind':
            #시리얼 라이즈에 보내니 위해 딕셔너리로 형식 바꿈
            post_serializer={
                "title" :request.data['title'],
                "content":request.data['content'],
                "category":category,
            }
            
            serializer = BlindPostSerialize(data = post_serializer)
            random_name_crated = random.choice(first) + random.choice(second)
            random_name = RandomName.objects.filter(random_name = random_name_crated).exists()

            if serializer.is_valid():
                serializer.save(user = request.user)
                print(serializer.data['id'])
                if random_name :
                    print('---while---')
                    while not random_name:
                        random_name_crated = random.choice(first) + random.choice(second)
                
                else:
                    RandomName.objects.create(
                    random_name = random_name_crated,
                    post_id = serializer.data['id'],
                    user = request.user
                    )
                context = {
                    'random_name': random_name_crated,
                    'post_data':serializer.data
                }
                return Response(context)
            else:
                return Response(serializer.errors)
            
    
    def get(self, request, category):

        #해결해야 할 부분(랜덤 닉네임을 어떻게 같이 보내줄 것인가.)
        post = Post.objects.filter(category = category)
        serialize = BlindPostListView(post, many=True)
        return Response(serialize.data)

# 디테일
class BlindPostDetailView(APIView):
    def get(self, request, post_id):
        postdetail = Post.objects.get(id = post_id)
        serialize = BlindPostDetailSerialize(postdetail)
        
        comment = PostComment.objects.filter(post_id = post_id)
        comment_serialize = BlindCommentPostSerialize(comment)
        context = {
            "comment": comment_serialize.data,
            "post":serialize.data
        }
        return Response(context)

    #수정

    def put(self, request, post_id):
        post_put = Post.objects.get(id = post_id)
        serialize = BlindPostSerialize(post_put, data = request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)

    #삭제
    def delete(self, request, post_id):
        try:
            post_delete = Post.objects.get(id = post_id)
            post_delete.delete()
        except:
            return Response('데이터가 없습니다.')
        return Response('삭제 완료')



#댓글 생성
class BlindComment(APIView):
    def post(self, request, post_id):
        post = Post.objects.get(id = post_id)
        print(post.id)
        comment_serializer={
                "content":request.data['content'],
                "post":post.id, #"post_id"라고 하면 값 안들어간다. "post"라고 모델과 똑같은 이름으로 해주어야 값이 들어간다.
            }
        serialize = BlindCommentPostSerialize(data = comment_serializer)
        
        random_name_crated = random.choice(first) + random.choice(second)
        random_name = RandomName.objects.filter(random_name = random_name_crated).exists()

        if serialize.is_valid():
            serialize.save(user=request.user)
            if random_name:
                while not random_name:
                    print('--while---')
                    random_name_crated = random.choice(first) + random.choice(second)
            else:
                print(post.id)
                RandomName.objects.create(
                    user = request.user,
                    post = Post.objects.get(id =post_id), 
                    # post_id, post.id를 하면 ValueError: Cannot assign "61": "RandomName.post" must be a "Post" instance. 가 된다.
                    random_name = random_name_crated
                )
            return Response(serialize.data)
        else:
            return Response(serialize.errors)


    
#수정/ 삭제
class BlindCommentChange(APIView):
    def put(self, request, comment_id):
        comment = PostComment.objects.get(id = comment_id)
        serializer = BlindCommentPostSerialize(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, comment_id):
        comment = PostComment.objects.get(id = comment_id)
        comment.delete()
        return Response('삭제완료')



#댓글 좋아요.
class CommentLikes(APIView):
    def post(self, request, comment_id):
        user = request.user
        like = Like.objects.filter(comment = comment_id, user = user).exists()
        if like:
            like.delete()
        else:
            like.create(comment = comment_id, user =user)
        
        

#게시글 좋아요
class PostLike(APIView):
    def post(self, request, post_id):
        user = request.user
        like = Like.objects.filter(post = post_id, user = user).exists()
        if like:
            like.delete()
        else:
            like.create(post = post_id, user =user)
