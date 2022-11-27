from rest_framework.generics import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, PostComment, RandomName
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import (CommentSerializer, 
CommentDetailSerializer, PostCreateSerializer, 
PostDetailSerializer, PostSearchSerializer, BlindCommentSerializer, BlindPostListSerializer, PostListSerializer, CommentDetailSerializer, TopPostListSerializer)
from django.db.models import Q # 검색
import random
from .randomname import randomname_list, randomname_list_2
from rest_framework.pagination import PageNumberPagination


# 인기글
class TopPostAPIView(APIView, PageNumberPagination):
    page_size=12
    def get(self, request):
        posts=Post.objects.all()
        post_list = posts.order_by('-created_date')

        b=[]
        for i in post_list:
            if i.likes.count() >= 0:
                b.append(i)
            else:
                print(b)
                pass
        results = self.paginate_queryset(b, request, view=self)
        serializer=TopPostListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
    

# 검색
class SearchAPIView(APIView, PageNumberPagination):
    page_size = 12

    def get(self, request, format=None):
        search=request.GET.get('search','')
        posts = Post.objects.all()
        post_list = posts.order_by('-created_date')

        if search:
            search_list = post_list.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            ).distinct()
            results = self.paginate_queryset(search_list, request, view=self)
            serializer=TopPostListSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)



class PostAPIView(APIView, PageNumberPagination):
    page_size = 12

    def post(self, request):
        category = request.data.get('category')
        print(category)
        serializer=PostCreateSerializer(data=request.data, partial=True)
        if serializer.is_valid():

            post=serializer.save(user=request.user)
            if category=='익명게시판':
                a = randomname_list
                b = randomname_list_2
                random_name=random.choice(a)+" "+random.choice(b)
                d=RandomName.objects.filter(name=random_name).exists() 
                if d==False:
                    RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                    return Response(status=status.HTTP_201_CREATED)         
                if d==True:
                    while True:
                        random_name=random.choice(a)+" "+random.choice(b)
                        exist=RandomName.objects.filter(name=random_name).exists() #get or create


                        if exist==False:
                            RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                            return Response(status=status.HTTP_201_CREATED)


                        elif exist==True:
                            continue
            else:
                return Response({"message":"게시글이 생성됨"},status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request):
        category_name=request.GET.get('category','')

        print(category_name)
        if category_name=='익명게시판':
            posts=Post.objects.all()
            category_list=posts.filter(category=category_name)
            time_list = category_list.order_by('-created_date')
            results = self.paginate_queryset(time_list, request, view=self)

            serializer=BlindPostListSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
        
        else:
            posts=Post.objects.all()
            category_list=posts.filter(category=category_name)
            time_list = category_list.order_by('-created_date')
            results = self.paginate_queryset(time_list, request, view=self)
            serializer=PostListSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)


# 댓글 작성, 리스트
# 글쓴이가 댓글달면 그냥 글쓴이로 표시해주거나 글쓴이가 댓글적었을때 랜덤이름이 안생기게 해줘야한다 
class CommentAPIView(APIView, PageNumberPagination):
    page_size=4
    def post(self, request, post_id):
        post=Post.objects.get(id=post_id)
        # post에 자기 id와 post를 가진 랜덤이름이 있다면 랜덤이름 안만들고 포스트를 저장

        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            if post.category == "익명게시판" and RandomName.objects.filter(user_id=request.user.id, post_id=post_id).exists() == False:
                a = randomname_list
                b = randomname_list_2
                random_name=random.choice(a)+" "+random.choice(b)
                c=RandomName.objects.filter(name=random_name).exists() 

                if c==False:
                    RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                    return Response(status=status.HTTP_201_CREATED)

                while True:
                    random_name=random.choice(a)+" "+random.choice(b)
                    c=RandomName.objects.filter(name=random_name).exists()
                    if c==True:
                        RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                    else:
                        continue

            else:
                return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        print(post_id)
        posts=Post.objects.get(id=post_id)
        comments=posts.postcomment_set.all()
        category_name=posts.category
        results = self.paginate_queryset(comments, request, view=self)

        print(category_name)
        if category_name=='익명게시판':
            serializer=BlindCommentSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        else:
            serializer=CommentSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)




# 게시글 상세, 수정, 삭제
class PostDetailAPIView(APIView): # 게시글 상세 / 수정 / 삭제
    def get(self, request, post_id): # 상세 페이지 들어왔을때
        post=get_object_or_404(Post, id=post_id)
        category_name=post.category
        try:
            post.hits = post.hits+1
            post.save()
        except:
            pass

        if category_name=='익명게시판':
            serializer=BlindPostListSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer=PostListSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)  


    def put(self, request, post_id): #수정
        post=get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            serializer=PostCreateSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, post_id): #삭제
        post=get_object_or_404(Post, id=post_id)
        if request.user==post.user: 
            post.delete()
            return Response("삭제완료",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)



class CommentDetailAPIView(APIView):
    def put(self, request, post_id, comment_id):
        comment=get_object_or_404(PostComment, id=comment_id)
        if request.user == comment.user:
            serializer=CommentDetailSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, post_id, comment_id): 
        comment=get_object_or_404(PostComment, id=comment_id)
        if request.user== comment.user:
            comment.delete()
            return Response("삭제완료",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)



# post like
class PostLikeAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post=get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response("좋아요 취소",status=status.HTTP_200_OK)

        else:
            post.likes.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)

# comment like
class CommentLikeAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id, post_id):
        comment=get_object_or_404(PostComment, id=comment_id) 
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response("좋아요 취소",status=status.HTTP_200_OK)

        else:
            comment.likes.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)