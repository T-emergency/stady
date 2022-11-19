from rest_framework.generics import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, PostComment, RandomName
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (CommentSerializer, 
CommentDetailSerializer, PostCreateSerializer, 
PostDetailSerializer, PostSearchSerializer, BlindCommentSerializer, BlindPostListSerializer, PostListSerializer, CommentDetailSerializer)
from django.db.models import Q # 검색
import random





# 인기글
class TopPostAPIView(APIView):
    def get(self, request):
        posts=Post.objects.all()
        b=[]
        for i in posts:
            if i.likes.count() > 40:
                b.append(i)
            else:
                print(b)
                pass

        serializer=PostListSerializer(b, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

# 검색
class SearchAPIView(APIView): 
    def get(self, request, format=None):
        search=request.GET.get('search','')
        print(search)
        list = Post.objects.all()
        print(list)
        if search:
            list = list.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            ).distinct()
            serializer=PostSearchSerializer(list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PostAPIView(APIView):
    def post(self, request, category_name): 
        category = request.data.get('category')
        serializer=PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post=serializer.save(user=request.user)
            print(post)
            print(post.id)
            if category=='blind':
                a = ['착잡한', '피곤한', '자상한', '포근한','귀여운','슬픈']
                b = ['할미꽃', '개망초','큰금계국', '백합', '수레국화']
                random_name=random.choice(a)+" "+random.choice(b)
                print("이름 만들기 시작")
                print(random_name)
                d=RandomName.objects.filter(name=random_name).exists() 
                print("존재하니?",d)
                if d==False:
                    RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                    print("없어서 만들고 끝냈어요", random_name)   
                    return Response(status=status.HTTP_201_CREATED)         
                if d==True:
                    while True: 
                        print("-------while--------")
                        random_name=random.choice(a)+" "+random.choice(b)
                        exist=RandomName.objects.filter(name=random_name).exists() #get or create
                        print(random_name)
                        print("같은 아이디가 존재하나요??", exist)

                        if exist==False:
                            RandomName.objects.create(name=random_name, post_id=post.id, user_id=request.user.id)
                            print("만들어졌어",random_name)
                            return Response(status=status.HTTP_201_CREATED)
                            

                        elif exist==True:
                            print("다시 돌아가서 만들어")
                            continue
            else:
                return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request, category_name):
        if category_name=='blind':
            posts=Post.objects.all()
            # print(posts)
            category_list=posts.filter(category=category_name)
            # print(category_list)
            serializer=BlindPostListSerializer(category_list, many=True)
            # print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            posts=Post.objects.all()
            # print(posts)
            category_list=posts.filter(category=category_name)
            # print(category_list)
            serializer=PostListSerializer(category_list, many=True)
            # print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)


# 댓글 작성, 리스트
class CommentAPIView(APIView):
    def post(self, request, post_id, comment_id):
        post=Post.objects.get(id=post_id)
        print(post)
        print(RandomName.objects.filter(post_id=post_id, user_id=request.user.id).exists())
        print(request.user.id)
        print(post_id)
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id) 
            if post.category == "blind":
                a = ['착잡한', '피곤한', '자상한', '포근한','귀여운','슬픈']
                b = ['할미꽃', '개망초','큰금계국', '백합', '수레국화']
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
        posts=Post.objects.get(id=post_id)
        comments=posts.postcomment_set.all()
        category_name=posts.category
        print(category_name)
        if category_name=='blind':
            serializer=BlindCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer=CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



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

        if category_name=='blind':
            serializer=BlindPostListSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer=PostDetailSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)  


    def put(self, request, post_id): #수정
        post=get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            serializer=PostCreateSerializer(post, data=request.data)
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