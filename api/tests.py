import email
from django.test import TestCase

# Create your tests here.

# from articles.models import Article, Comment
from user.models import User
from study_group.models import Study


from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class SetUpTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.study_data = {
            "title" : "축구할 사람?",
            "content" : "일단 난 못해",
            "on_off_line": False,
            "headcount" : 22
        }
        cls.log_data = {}
        cls.user_data = {
            "username" : "tester11",
            "password" : "123",
            "email" : "test@naver.com"
        }
        cls.user = User.objects.create_user(
            username = cls.user_data["username"],
            password = cls.user_data["password"],
            email = cls.user_data["email"]
        )
        cls.study = Study.objects.create(
            user = cls.user,
            title = cls.study_data["title"],
            content = cls.study_data["content"],
            on_off_line = cls.study_data["on_off_line"]
        )
    
    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.data).data["access"]




class StudyListTest(SetUpTest):
    pass