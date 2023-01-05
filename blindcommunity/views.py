from rest_framework.generics import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, PostComment, RandomName
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (CommentSerializer, PostCreateSerializer, CommentDetailSerializer, BlindCommentSerializer, BlindPostListSerializer, PostListSerializer, TopPostListSerializer)
from django.db.models import Q
import random
from .randomname import randomname_list, randomname_list_2
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse, JsonResponse


# 인기글
class TopPostAPIView(APIView, PageNumberPagination):
    page_size=12
    def get(self, request):
        posts=Post.objects.all()
        post_list = posts.order_by('-created_date')

        top_list=[]
        for i in post_list:
            if i.likes.count() >= 0:
                top_list.append(i)
                print(i)
            else:
                
                pass
        results = self.paginate_queryset(top_list, request, view=self)
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
                random_adjective = randomname_list
                random_noun = randomname_list_2
                random_name=random.choice(random_adjective)+" "+random.choice(random_noun)
                d=RandomName.objects.filter(name=random_name).exists() 
                if d==False:
                    RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                    return Response(status=status.HTTP_201_CREATED)         
                if d==True:
                    while True:
                        random_name=random.choice(random_adjective)+" "+random.choice(random_noun)
                        exist=RandomName.objects.filter(name=random_name).exists()


                        if exist==False:
                            RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                            return Response(status=status.HTTP_201_CREATED)


                        elif exist==True:
                            continue
            else:
                return Response({"message":"게시글이 생성됨"},status=status.HTTP_201_CREATED)
        else:
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
class CommentAPIView(APIView, PageNumberPagination):
    page_size=4
    def post(self, request, post_id):
        post=Post.objects.get(id=post_id)

        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            if post.category == "익명게시판" and RandomName.objects.filter(user_id=request.user.id, post_id=post_id).exists() == False:
                random_adjective = randomname_list
                random_noun = randomname_list_2
                random_name=random.choice(random_adjective)+" "+random.choice(random_noun)
                c=RandomName.objects.filter(name=random_name).exists() 

                if c==False:
                    RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                    return Response(status=status.HTTP_201_CREATED)

                while True:
                    random_name=random.choice(random_adjective)+" "+random.choice(random_noun)
                    c=RandomName.objects.filter(name=random_name).exists() 

                    if c==False:
                        RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                    else:
                        continue

            else:
                return Response(status=status.HTTP_201_CREATED)

        else:
            print('is not valid')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        posts=Post.objects.get(id=post_id)
        comments=posts.postcomment_set.all()
        category_name=posts.category
        results = self.paginate_queryset(comments, request, view=self)

        if category_name=='익명게시판':
            serializer=BlindCommentSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        else:
            serializer=CommentSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)


        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0]
        #     print("아이피1",ip)
        #     print("아이피2",x_forwarded_for)
        # else:
        #     ip = request.META.get('REMOTE_ADDR')
        #     print("아이피3",ip)
        #     print("아이피4",x_forwarded_for)
import datetime
from django.db import transaction
from django.http import HttpResponse, HttpRequest
# 게시글 상세, 수정, 삭제
class PostDetailAPIView(APIView):
    @transaction.atomic
    def get(self, request, post_id):
        instance=get_object_or_404(Post, id=post_id)
        # 당일날 밤 12시에 쿠키 초기화
        tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        
        # response를 미리 받고 쿠키를 만들어야 한다
        serializer=BlindPostListSerializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        
        # 쿠키 읽기 & 생성
        if request.COOKIES.get('hit') is not None: # 쿠키에 hit 값이 이미 있을 경우
            cookies = request.COOKIES.get('hit')
            cookies_list = cookies.split('|') # '|'는 다르게 설정 가능 ex) '.'
            if str(post_id) not in cookies_list:
                response.set_cookie('hit', cookies+f'|{post_id}', expires=expires) # 쿠키 생성
                with transaction.atomic(): # 모델 필드인 views에 1 추가
                    instance.hits += 1
                    instance.save()
                    
        else: # 쿠키에 hit 값이 없을 경우(즉 현재 보는 게시글이 첫 게시글임)
            print("첫 쿠키")
            response.set_cookie('hit', post_id, expires=expires)
            instance.hits += 1
            instance.save()

        # views가 추가되면 해당 instance를 serializer에 표시
        serializer=BlindPostListSerializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        print(request.COOKIES)
        # print(HttpResponse.COOKIES)
        print(request.header)
        return response
        # category_name=post.category
        # tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
        # expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        # if category_name=='익명게시판':
        #     cookies_item=''
        #     cookie_name='hits'
        #     serializer=BlindPostListSerializer(post)
        #     print("0",request.COOKIES.get(cookie_name))
        #     response = Response(serializer.data, status=status.HTTP_200_OK)
        #     if request.COOKIES.get(cookie_name) is not None: # 쿠기에 hit있다면
        #         cookies = request.COOKIES.get(cookie_name)
        #         cookies_list = cookies.split('|')
        #         print("1",cookies_list)
        #         if str(post_id) not in cookies_list: # 쿠키리스트에 post id 없다면
        #             cookies_item=f'{cookies}|{post_id}'
        #             post.hits=post.hits+1
        #             post.save()
        #     else: #hits 없다면
        #         response.set_cookie(cookie_name, post_id, expires=expires)
        #         post.hits=post.hits+1
        #         post.save()
        #         print("else")
        #     # if cookies_item:
        #     #     print("3",cookies_item)
        #     #     good=response.set_cookie(cookie_name, cookies_item, expires=expires)
        #     #     print(good)
        #     serializer=BlindPostListSerializer(post)
        #     response = Response(serializer.data, status=status.HTTP_200_OK)
        #     return response
        # else:
        #     serializer=PostListSerializer(post)
        #     return Response(serializer.data, status=status.HTTP_200_OK)  


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

    def post(self, request, comment_id, post_id):
        comment=get_object_or_404(PostComment, id=comment_id) 
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response("좋아요 취소",status=status.HTTP_200_OK)

        else:
            comment.likes.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)