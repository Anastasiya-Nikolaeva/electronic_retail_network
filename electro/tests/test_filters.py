# from django.urls import reverse
# from rest_framework import status
# from django.contrib.auth import get_user_model
# from rest_framework.test import APITestCase
# from rest_framework_simplejwt.tokens import RefreshToken
#
# from electro.models import NetworkNode, Supplier, Product
#
#
# class NetworkNodeFilterTests(APITestCase):
#     def setUp(self):
#         User = get_user_model()
#
#         # Создание тестового пользователя с email и username
#         self.user = User.objects.create_user(
#             email='testuser@example.com',
#             username='testuser',
#             password='testpassword'
#         )
#         self.user.is_active = True  # Убедитесь, что пользователь активен
#         self.user.save()
#
#         # Получение JWT токена
#         self.token = RefreshToken.for_user(self.user).access_token
#
#         # Создание тестовых данных для продуктов
#         product1 = Product.objects.create(name="Продукт 1", model="Модель 1", release_date="2025-01-01")
#         product2 = Product.objects.create(name="Продукт 2", model="Модель 2", release_date="2025-02-01")
#         product3 = Product.objects.create(name="Продукт 3", model="Модель 3", release_date="2025-03-01")
#
#         # Создание узлов сети
#         supplier1 = Supplier.objects.create(name="Поставщик 1")
#         supplier2 = Supplier.objects.create(name="Поставщик 2")
#         supplier3 = Supplier.objects.create(name="Поставщик 3")
#
#         NetworkNode.objects.create(
#             name="Узел 1",
#             email="node1@example.com",
#             country="Россия",
#             city="Москва",
#             street="Ленина",
#             house_number="1",
#             product=product1,
#             product_name="Продукт 1",
#             product_model="Модель 1",
#             product_release_date="2025-01-01",
#             supplier=supplier1,
#             level=0
#         )
#         NetworkNode.objects.create(
#             name="Узел 2",
#             email="node2@example.com",
#             country="Россия",
#             city="Санкт-Петербург",
#             street="Пушкина",
#             house_number="2",
#             product=product2,
#             product_name="Продукт 2",
#             product_model="Модель 2",
#             product_release_date="2025-02-01",
#             supplier=supplier2,
#             level=1
#         )
#         NetworkNode.objects.create(
#             name="Узел 3",
#             email="node3@example.com",
#             country="США",
#             city="Нью-Йорк",
#             street="Бродвей",
#             house_number="3",
#             product=product3,
#             product_name="Продукт 3",
#             product_model="Модель 3",
#             product_release_date="2025-03-01",
#             supplier=supplier3,
#             level=2
#         )
#
#     def test_filter_by_country(self):
#         url = reverse('electro:networknode-list')
#         response = self.client.get(url, {'country': 'Россия'}, HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)  # Должно вернуть 2 узла
#
#     def test_filter_by_city(self):
#         url = reverse('electro:networknode-list')
#         response = self.client.get(url, {'city': 'Москва'}, HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # Должно вернуть 1 узел
#
#     def test_filter_by_country_and_city(self):
#         url = reverse('electro:networknode-list')
#         response = self.client.get(url, {'country': 'Россия', 'city': 'Москва'}, HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # Должно вернуть 1 узел