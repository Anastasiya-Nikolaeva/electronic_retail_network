from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class CustomUserViewSetTests(APITestCase):
    """
    Тестовый класс для вьюсета CustomUserViewSet.

    Этот класс содержит тесты для проверки операций CRUD (создание, чтение, обновление, удаление)
    для модели CustomUser через API.
    """

    def setUp(self):
        """
        Настройка тестового окружения.

        Создает тестового пользователя и аутентифицирует его для использования в тестах.
        """
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", username="testuser", password="testpassword"
        )
        self.client.login(email="testuser@example.com", password="testpassword")
        self.url = reverse(
            "users:customuser-list"
        )  # Убедитесь, что это правильный URL для вашего вьюсета

    def test_create_user(self):
        """
        Тестирование создания нового пользователя через API.

        Проверяет, что можно создать нового пользователя с валидными данными.
        """
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newsecurepassword",
            "phone": "1234567890",
            "city": "New City",
            "avatar": None,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            CustomUser.objects.count(), 2
        )  # Проверка, что пользователь создан
        self.assertEqual(
            CustomUser.objects.get(id=response.data["id"]).email, data["email"]
        )

    def test_list_users(self):
        """
        Тестирование получения списка пользователей через API.

        Проверяет, что можно получить список пользователей.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Проверка, что возвращается один пользователь

    def test_update_user(self):
        """
        Тестирование обновления существующего пользователя через API.

        Проверяет, что можно обновить данные существующего пользователя.
        """
        user_to_update = CustomUser.objects.create_user(
            email="updateuser@example.com",
            username="updateuser",
            password="updatepassword",
        )
        update_url = reverse(
            "users:customuser-detail", args=[user_to_update.id]
        )  # Убедитесь, что это правильный URL
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "password": "newsecurepassword",
            "phone": "0987654321",
            "city": "Updated City",
            "avatar": None,
        }
        response = self.client.put(update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_to_update.refresh_from_db()
        self.assertEqual(user_to_update.username, data["username"])
        self.assertEqual(user_to_update.email, data["email"])

    def test_delete_user(self):
        """
        Тестирование удаления пользователя через API.

        Проверяет, что можно удалить существующего пользователя.
        """
        user_to_delete = CustomUser.objects.create_user(
            email="deleteuser@example.com",
            username="deleteuser",
            password="deletepassword",
        )
        delete_url = reverse(
            "users:customuser-detail", args=[user_to_delete.id]
        )  # Убедитесь, что это правильный URL
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            CustomUser.objects.count(), 1
        )  # Проверка, что пользователь удален
