from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class IsActiveEmployeePermissionTests(APITestCase):
    """
    Тестовый класс для проверки разрешения IsActiveEmployee.

    Этот класс содержит тесты для проверки доступа к представлениям
    в зависимости от состояния пользователя (активный или неактивный).
    """

    def setUp(self):
        """
        Настройка тестового окружения.

        Создает активного и неактивного пользователя для использования в тестах.
        """
        self.active_user = CustomUser.objects.create_user(
            email="activeuser@example.com",
            username="activeuser",
            password="activepassword",
        )
        self.inactive_user = CustomUser.objects.create_user(
            email="inactiveuser@example.com",
            username="inactiveuser",
            password="inactivepassword",
        )
        self.inactive_user.is_active = False
        self.inactive_user.save()

        self.url = reverse(
            "users:customuser-list"
        )  # Убедитесь, что это правильный URL для вашего вьюсета

    def test_active_user_access(self):
        """
        Тестирование доступа активного пользователя.

        Проверяет, что активный пользователь имеет доступ к представлению.
        """
        self.client.login(email="activeuser@example.com", password="activepassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inactive_user_access(self):
        """
        Тестирование доступа неактивного пользователя.

        Проверяет, что неактивный пользователь не может аутентифицироваться.
        """
        # Не аутентифицируем неактивного пользователя
        response = self.client.login(
            email="inactiveuser@example.com", password="inactivepassword"
        )
        self.assertFalse(response)  # Ожидаем, что аутентификация не удалась

        # Теперь проверяем доступ к представлению
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )  # Ожидаем 401

    def test_unauthenticated_user_access(self):
        """
        Тестирование доступа неаутентифицированного пользователя.

        Проверяет, что неаутентифицированный пользователь не имеет доступа к представлению.
        """
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )  # Ожидаем 401
