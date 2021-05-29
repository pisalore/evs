import json
from PIL import Image
from io import BytesIO
from users.models import EvUser
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status


class LogInTest(TestCase):
    redirect_url = '/'

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        EvUser.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response=response, expected_url=self.redirect_url)


class RegistrationTest(TestCase):
    redirect_url = '/'

    def test_user_registration(self):
        url = '/accounts/register/user/'
        user_data = {
            'first_name': 'test',
            'last_name': 'user',
            'birthday': '1995-04-13',
            'city': 'test_city',
            'username': 'test_username',
            'email': 'test@test.it',
            'password1': 'averystrongPassword123',
            'password2': 'averystrongPassword123'
        }

        response = self.client.post(url, user_data)
        self.assertRedirects(response=response, expected_url=self.redirect_url)

    def test_organizer_registration(self):
        url = '/accounts/register/organizer/'
        organizer_data = {
            'organization_name': 'test',
            'username': 'city_username',
            'email': 'test@organization.it',
            'password1': 'averystrongPassword123',
            'password2': 'averystrongPassword123'
        }

        response = self.client.post(url, organizer_data)
        self.assertRedirects(response=response, expected_url=self.redirect_url)


class RetrieveUserInfoTest(APITestCase):
    user_url = '/api/user/'

    def setUp(self):
        self.user = EvUser.objects.create_user(username="test",
                                               password='test_password123',
                                               email="test@mail.it",
                                               is_organizer=False,
                                               profile_image=None)
        self.organizer = EvUser.objects.create_user(username="test_org",
                                                    organization_name="org",
                                                    password='test_password123',
                                                    email="test_org@mail.it",
                                                    is_organizer=True,
                                                    profile_image=None)

    def test_retrieve_user_main_info(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {"username": "test",
             "organization_name": "",
             "is_organizer": False,
             "profile_image": None})

    def test_retrieve_organizer_main_info(self):
        self.client.force_authenticate(user=self.organizer)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {"username": "test_org",
             "organization_name": "org",
             "is_organizer": True,
             "profile_image": None, })


class UploadFileTest(APITestCase):
    def setUp(self):
        self.user = EvUser.objects.create_user(username="test",
                                               password='test_password123',
                                               email="test@mail.it",
                                               is_organizer=False,
                                               profile_image=None)
        self.url = "/api/user/profile-image/"

    def test_image_upload(self):
        self.client.force_authenticate(user=self.user)

        stream = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(stream, format='jpeg')

        uploaded_file = SimpleUploadedFile("file.jpg", stream.getvalue(), content_type="image/jpg")
        data = {
            "profile_image.type": "PI",
            "profile_image.document": uploaded_file,
            "profile_image.loaded_by": self.user.id
        }

        response = self.client.put(self.url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
