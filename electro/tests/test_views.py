from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from electro.models import NetworkNode, Payment, Product, Supplier


class SupplierViewSetTests(APITestCase):
    def setUp(self):
        """Настройка тестов, создание пользователя и поставщика."""
        # Сбрасываем базу данных
        call_command("flush", "--noinput")  # Удаляет все данные из базы данных

        User = get_user_model()
        self.user = User.objects.create_user(
            username="тестовый_пользователь",
            email="testuser@example.com",
            password="testpassword",
            is_active=True,
        )

        # Получаем JWT-токен
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Устанавливаем токен в заголовки
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        self.url = reverse("electro:supplier-list")
        self.valid_data = {
            "name": "Поставщик A",
            "email": "supplier_a@example.com",  # Уникальный email
            "country": "Страна A",
            "city": "Город A",
            "street": "Улица A",
            "house_number": "1A",
            "debt": 100.00,
        }
        self.invalid_data = {
            "name": "",
            "email": "некорректный_email",
            "country": "Страна B",
            "city": "Город B",
            "street": "Улица B",
            "house_number": "2B",
            "debt": 100.00,
        }

        # Создаем существующего поставщика для тестов
        self.existing_supplier = Supplier.objects.create(
            name="Поставщик B",
            email="supplier_b@example.com",
            country="Страна B",
            city="Город B",
            street="Улица B",
            house_number="2B",
            debt=50.00,
        )

    def test_create_supplier(self):
        """Настройка тестов, создание пользователя и поставщика."""
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_supplier_with_existing_email(self):
        """Тестирование создания нового поставщика с уже существующим email."""
        duplicate_data = self.valid_data.copy()
        duplicate_data["email"] = (
            "supplier_b@example.com"  # Используем существующий email
        )
        response = self.client.post(self.url, duplicate_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_supplier(self):
        """Тестирование обновления существующего поставщика."""
        update_data = {
            "name": "Обновленный Поставщик A",
            "email": "updated_supplier_a@example.com",
            "country": "Страна A",
            "city": "Город A",
            "street": "Улица A",
            "house_number": "1A",
        }
        response = self.client.put(
            reverse("electro:supplier-detail", args=[self.existing_supplier.id]),
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_supplier.refresh_from_db()
        self.assertEqual(self.existing_supplier.name, "Обновленный Поставщик A")
        self.assertEqual(self.existing_supplier.email, "updated_supplier_a@example.com")

    def test_update_supplier_invalid_data(self):
        """Тестирование обновления поставщика с некорректными данными."""
        response = self.client.put(
            reverse("electro:supplier-detail", args=[self.existing_supplier.id]),
            self.invalid_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_supplier_with_existing_email(self):
        """Тестирование обновления поставщика с уже существующим email."""
        another_supplier = Supplier.objects.create(
            name="Поставщик C",
            email="supplier_c@example.com",  # Уникальный email
            country="Страна C",
            city="Город C",
            street="Улица C",
            house_number="3C",
            debt=50.00,
        )
        update_data = self.valid_data.copy()
        update_data["email"] = another_supplier.email  # Используем существующий email
        response = self.client.put(
            reverse("electro:supplier-detail", args=[self.existing_supplier.id]),
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_supplier(self):
        """Тестирование удаления существующего поставщика."""
        response = self.client.delete(
            reverse("electro:supplier-detail", args=[self.existing_supplier.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)  # Проверяем, что поставщик удален


class ProductViewSetTests(APITestCase):
    def setUp(self):
        """Настройка тестов, создание пользователя и продукта."""
        User = get_user_model()
        self.user = User.objects.create_user(
            username="тестовый_пользователь",
            email="testuser@example.com",
            password="testpassword",
            is_active=True,  # Убедитесь, что пользователь активен
        )

        # Получаем JWT-токен
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Устанавливаем токен в заголовки
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        self.url = reverse(
            "electro:product-list"
        )  # Убедитесь, что URL соответствует вашему маршруту
        self.valid_data = {
            "name": "Продукт A",
            "model": "Модель A",
            "release_date": "2025-01-01",
        }
        self.invalid_data = {
            "name": "",
            "model": "Модель B",
            "release_date": "некорректная_дата",
        }

        # Создаем существующий продукт для тестов
        self.existing_product = Product.objects.create(
            name="Продукт B", model="Модель B", release_date="2025-01-01"
        )

    def test_create_product(self):
        """Тестирование создания нового продукта."""
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)  # Проверяем, что продукт добавлен

    def test_create_product_invalid_data(self):
        """Тестирование создания продукта с некорректными данными."""
        response = self.client.post(self.url, self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_products(self):
        """Тестирование получения списка продуктов."""
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Проверяем, что возвращается один продукт

    def test_update_product(self):
        """Тестирование обновления существующего продукта."""
        update_data = {
            "name": "Обновленный Продукт B",
            "model": "Обновленная Модель B",
            "release_date": "2025-01-02",
        }
        response = self.client.put(
            reverse("electro:product-detail", args=[self.existing_product.id]),
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_product.refresh_from_db()
        self.assertEqual(self.existing_product.name, "Обновленный Продукт B")

    def test_update_product_invalid_data(self):
        """Тестирование обновления продукта с некорректными данными."""
        response = self.client.put(
            reverse("electro:product-detail", args=[self.existing_product.id]),
            self.invalid_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        """Тестирование удаления существующего продукта."""
        response = self.client.delete(
            reverse("electro:product-detail", args=[self.existing_product.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)  # Проверяем, что продукт удален


class NetworkNodeViewSetTests(APITestCase):
    def setUp(self):
        """Настройка тестов, создание пользователя, продукта и поставщика."""
        User = get_user_model()
        self.user = User.objects.create_user(
            username="тестовый_пользователь",
            email="testuser@example.com",
            password="testpassword",
            is_active=True,  # Убедитесь, что пользователь активен
        )

        # Получаем JWT-токен
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Устанавливаем токен в заголовки
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        # Создаем продукт и поставщика для тестов
        self.product = Product.objects.create(
            name="Продукт A", model="Модель A", release_date="2025-01-01"
        )
        self.supplier = Supplier.objects.create(
            name="Поставщик A",
            email="supplier_a@example.com",
            country="Страна A",
            city="Город A",
            street="Улица A",
            house_number="1A",
            debt=0.00,
        )

        self.url = reverse(
            "electro:networknode-list"
        )  # Убедитесь, что URL соответствует вашему маршруту
        self.valid_data = {
            "name": "Узел Сети A",
            "email": "node_a@example.com",
            "country": "Страна A",
            "city": "Город A",
            "street": "Улица A",
            "house_number": "1A",
            "product": self.product.id,
            "product_name": self.product.name,
            "product_model": self.product.model,
            "product_release_date": self.product.release_date,
            "supplier": self.supplier.id,
            "debt": 100.00,
            "level": 0,
        }
        self.invalid_data = {
            "name": "",
            "email": "некорректный_email",
            "country": "Страна B",
            "city": "Город B",
            "street": "Улица B",
            "house_number": "2B",
            "product": self.product.id,
            "supplier": self.supplier.id,
            "debt": 100.00,
            "level": 0,
        }

        # Создаем существующий узел сети для тестов
        self.existing_node = NetworkNode.objects.create(
            name="Узел Сети B",
            email="node_b@example.com",
            country="Страна B",
            city="Город B",
            street="Улица B",
            house_number="2B",
            product=self.product,
            product_name=self.product.name,
            product_model=self.product.model,
            product_release_date=self.product.release_date,
            supplier=self.supplier,
            debt=50.00,
            level=1,
        )

    def test_create_network_node(self):
        """Тестирование создания нового узла сети."""
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkNode.objects.count(), 2)  # Проверяем, что узел добавлен

    def test_create_network_node_invalid_data(self):
        """Тестирование создания узла сети с некорректными данными."""
        response = self.client.post(self.url, self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_network_nodes(self):
        """Тестирование получения списка узлов сети."""
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что возвращается один узел

    def test_update_network_node(self):
        """Тестирование обновления существующего узла сети."""
        update_data = {
            "name": "Обновленный Узел Сети B",
            "email": "updated_node_b@example.com",
            "country": "Страна B",
            "city": "Город B",
            "street": "Улица B",
            "house_number": "2B",
            "product": self.product.id,
            "product_name": self.product.name,
            "product_model": self.product.model,
            "product_release_date": self.product.release_date,
            "supplier": self.supplier.id,
            "debt": 25.00,
            "level": 1,
        }
        response = self.client.put(
            reverse("electro:networknode-detail", args=[self.existing_node.id]),
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_node.refresh_from_db()
        self.assertEqual(self.existing_node.name, "Обновленный Узел Сети B")
        self.assertEqual(self.existing_node.debt, 25.00)

    def test_update_network_node_invalid_data(self):
        """Тестирование обновления узла сети с некорректными данными."""
        response = self.client.put(
            reverse("electro:networknode-detail", args=[self.existing_node.id]),
            self.invalid_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_network_node(self):
        """Тестирование удаления существующего узла сети."""
        response = self.client.delete(
            reverse("electro:networknode-detail", args=[self.existing_node.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NetworkNode.objects.count(), 0)  # Проверяем, что узел удален

    def test_clear_debt(self):
        """Тестирование очистки задолженности узла сети."""
        response = self.client.post(
            reverse("electro:networknode-clear-debt", args=[self.existing_node.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_node.refresh_from_db()
        self.assertEqual(
            self.existing_node.debt, 0.00
        )  # Проверяем, что задолженность очищена

    def test_clear_debt_already_zero(self):
        """Тестирование попытки очистки задолженности, когда она уже равна нулю."""
        self.existing_node.debt = 0.00
        self.existing_node.save()
        response = self.client.post(
            reverse("electro:networknode-clear-debt", args=[self.existing_node.id])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "Задолженность уже равна нулю")


class PaymentViewSetTests(APITestCase):
    def setUp(self):
        """Настройка тестов, создание пользователя, продукта, поставщика и узла сети."""
        User = get_user_model()
        self.user = User.objects.create_user(
            username="тестовый_пользователь",
            email="testuser@example.com",
            password="testpassword",
            is_active=True,  # Убедитесь, что пользователь активен
        )

        # Получаем JWT-токен
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Устанавливаем токен в заголовки
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        # Создаем продукт, поставщика и узел сети для тестов
        self.product = Product.objects.create(
            name="Продукт A", model="Модель A", release_date="2025-01-01"
        )
        self.supplier = Supplier.objects.create(
            name="Поставщик A",
            email="supplier_a@example.com",
            country="Страна A",
            city="Город A",
            street="Улица A",
            house_number="1A",
            debt=100.00,  # Установим задолженность
        )
        self.network_node = NetworkNode.objects.create(
            name="Узел Сети A",
            email="node_a@example.com",
            country="Страна A",
            city="Город A",
            street="Улица A",
            house_number="1A",
            product=self.product,
            product_name=self.product.name,
            product_model=self.product.model,
            product_release_date=self.product.release_date,
            supplier=self.supplier,
            debt=0.00,
            level=0,
        )

        self.url = reverse(
            "electro:payment-list"
        )  # Убедитесь, что URL соответствует вашему маршруту
        self.valid_data = {
            "supplier": self.supplier.id,
            "network_node": self.network_node.id,
            "amount": 50.00,
            "description": "Оплата за услуги",
        }
        self.invalid_data = {
            "supplier": self.supplier.id,
            "network_node": self.network_node.id,
            "amount": 150.00,  # Сумма превышает задолженность
            "description": "Оплата за услуги",
        }

        # Создаем существующий платеж для тестов
        self.existing_payment = Payment.objects.create(
            supplier=self.supplier,
            network_node=self.network_node,
            amount=50.00,
            description="Первый платеж",
        )

    def test_create_payment(self):
        """Тестирование создания нового платежа."""
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)  # Проверяем, что платеж добавлен

    def test_create_payment_exceeding_debt(self):
        """Тестирование создания платежа, сумма которого превышает задолженность поставщика."""
        response = self.client.post(self.url, self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)  # Проверяем, что ошибка присутствует

    def test_list_payments(self):
        """Тестирование получения списка платежей."""
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Проверяем, что возвращается один платеж

    def test_update_payment(self):
        """Тестирование обновления существующего платежа."""
        update_data = {
            "supplier": self.supplier.id,
            "network_node": self.network_node.id,
            "amount": 75.00,
            "description": "Обновленный платеж",
        }
        response = self.client.put(
            reverse("electro:payment-detail", args=[self.existing_payment.id]),
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_payment.refresh_from_db()
        self.assertEqual(self.existing_payment.amount, 75.00)

    def test_delete_payment(self):
        """Тестирование удаления существующего платежа."""
        response = self.client.delete(
            reverse("electro:payment-detail", args=[self.existing_payment.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payment.objects.count(), 0)  # Проверяем, что платеж удален

    def test_create_payment_without_supplier(self):
        """Тестирование создания платежа без указания поставщика."""
        data_without_supplier = {
            "network_node": self.network_node.id,
            "amount": 50.00,
            "description": "Оплата без поставщика",
        }
        response = self.client.post(self.url, data_without_supplier, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("supplier", response.data)  # Проверяем, что ошибка присутствует

    def test_create_payment_without_network_node(self):
        """Тестирование создания платежа без указания узла сети."""
        data_without_network_node = {
            "supplier": self.supplier.id,
            "amount": 50.00,
            "description": "Оплата без узла сети",
        }
        response = self.client.post(self.url, data_without_network_node, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "network_node", response.data
        )  # Проверяем, что ошибка присутствует
        self.assertEqual(
            response.data["network_node"][0], "Это поле обязательно."
        )  # Проверяем сообщение об ошибке
