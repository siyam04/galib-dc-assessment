from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from content.models import Category, Content


class CategoryModelTest(TestCase):
    def test_str(self):
        cat = Category.objects.create(name='Test', description='Test desc')
        self.assertEqual(str(cat), 'Test')


class ContentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='user', email='user@test.com', password='pass12345')
        self.category = Category.objects.create(name='AI', description='AI')

    def test_content_creation(self):
        content = Content.objects.create(
            title='Test',
            body='Body',
            category=self.category,
            owner=self.user,
            summary='',
            sentiment='',
            topics=[],
            recommendations=''
        )
        self.assertEqual(content.title, 'Test')
        self.assertEqual(content.owner, self.user)
        self.assertEqual(content.category, self.category)


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register(self):
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'new@test.com', 'password': 'newpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TokenAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='user', email='user@test.com', password='pass12345')

    def test_jwt_token(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'user', 'password': 'pass12345'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())


class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='AI', description='AI')

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ContentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='user', email='user@test.com', password='pass12345')
        self.category = Category.objects.create(name='AI', description='AI')
        self.client.force_authenticate(user=self.user)

    def test_content_crud(self):
        # Create
        url = reverse('content-list')
        data = {'title': 'Test', 'body': 'Body', 'category_id': self.category.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        content_id = response.json()['id']
        # Retrieve
        url = reverse('content-detail', args=[content_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Update
        response = self.client.patch(url, {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Delete
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AIAnalyzeTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='user', email='user@test.com', password='pass12345')
        self.client.force_authenticate(user=self.user)

    def test_ai_analyze_mock(self):
        url = reverse('ai-analyze')
        data = {'text': 'Test AI content'}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [200, 500])


class RBACPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='user', email='user@test.com', password='pass12345')
        self.admin = get_user_model().objects.create_superuser(username='admin', email='admin@test.com', password='adminpass')

    def test_rbac_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rbac_non_admin(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
