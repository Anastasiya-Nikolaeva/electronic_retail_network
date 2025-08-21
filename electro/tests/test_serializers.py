# from decimal import Decimal
#
# from django.test import TestCase
# from django.utils import timezone
#
# from electro.models import NetworkNode, Product, Supplier
# from electro.serializers import (NetworkNodeSerializer, PaymentSerializer,
#                                  ProductSerializer, SupplierSerializer)
#
#
# class SupplierSerializerTest(TestCase):
#     def setUp(self):
#         """Создание тестового поставщика для использования в тестах."""
#         self.supplier = Supplier.objects.create(
#             name="Поставщик",
#             email="supplier@example.com",
#             country="Россия",
#             city="Ростов на дону",
#             street="Ростовская",
#             house_number="1",
#             debt=Decimal("100.00"),
#         )
#
#     def test_supplier_serializer_create(self):
#         """Тестирование создания нового поставщика через сериализатор."""
#         data = {
#             "name": "Новый поставщик",
#             "email": "new@example.com",
#             "country": "Россия",
#             "city": "Ростов на дону",
#             "street": "Ростовская",
#             "house_number": "2",
#             "debt": 50.00,
#         }
#         serializer = SupplierSerializer(data=data)
#         self.assertTrue(serializer.is_valid())
#         supplier = serializer.save()
#         self.assertEqual(supplier.name, "Новый поставщик")
#
#     def test_supplier_serializer_email_unique(self):
#         """Тестирование уникальности email для поставщика."""
#         data = {
#             "name": "Другой поставщик",
#             "email": "supplier@example.com",  # Используем существующий email
#             "country": "Россия",
#             "city": "Ростов на дону",
#             "street": "Ростовская",
#             "house_number": "3",
#             "debt": 50.00,
#         }
#         serializer = SupplierSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn("email", serializer.errors)
#
#     def test_supplier_serializer_update(self):
#         """Тестирование обновления существующего поставщика через сериализатор."""
#         data = {
#             "name": "Обновленный поставщик",
#             "email": "supplier@example.com",
#             "country": "Россия",
#             "city": "Ростов на дону",
#             "street": "Ростовская",
#             "house_number": "4",
#             "debt": 100.00,
#         }
#         serializer = SupplierSerializer(instance=self.supplier, data=data)
#         self.assertTrue(serializer.is_valid())
#         updated_supplier = serializer.save()
#         self.assertEqual(updated_supplier.name, "Обновленный поставщик")
#
#
# class ProductSerializerTest(TestCase):
#     def setUp(self):
#         """Создание тестовых данных для продукта."""
#         self.valid_data = {
#             "name": "Тестовый продукт",
#             "model": "TP-100",
#             "release_date": "2025-01-01",
#         }
#         self.serializer = ProductSerializer(data=self.valid_data)
#
#     def test_serializer_valid(self):
#         """Тестирование валидности сериализатора с корректными данными."""
#         self.assertTrue(self.serializer.is_valid())
#
#     def test_serializer_invalid_future_release_date(self):
#         """Тестирование сериализатора с датой выпуска в будущем."""
#         future_date = timezone.now().date() + timezone.timedelta(days=1)
#         invalid_data = self.valid_data.copy()
#         invalid_data["release_date"] = future_date
#         self.serializer = ProductSerializer(data=invalid_data)
#         self.assertFalse(self.serializer.is_valid())
#         self.assertIn("release_date", self.serializer.errors)
#         self.assertEqual(
#             self.serializer.errors["release_date"][0],
#             "Дата выпуска не может быть в будущем.",
#         )
#
#     def test_serializer_invalid_missing_fields(self):
#         """Тестирование сериализатора с отсутствующими обязательными полями."""
#         invalid_data = {"model": "TP-100", "release_date": "2025-01-01"}
#         self.serializer = ProductSerializer(data=invalid_data)
#         self.assertFalse(self.serializer.is_valid())
#         self.assertIn("name", self.serializer.errors)
#
#
# class NetworkNodeSerializerTest(TestCase):
#     def setUp(self):
#         """Создание тестовых данных для узла сети."""
#         self.supplier = Supplier.objects.create(name="Тестовый поставщик")
#         self.product = Product.objects.create(
#             name="Тестовый продукт", release_date="2025-01-01"
#         )
#         self.valid_data = {
#             "name": "Тестовый узел",
#             "email": "test@example.com",
#             "country": "Россия",
#             "city": "Ростов на дону",
#             "street": "Тестовая улица",
#             "house_number": "1",
#             "product": self.product.id,
#             "product_name": "Тестовый продукт",
#             "product_model": "TP-100",
#             "supplier": self.supplier.id,
#             "level": 0,
#         }
#         self.serializer = NetworkNodeSerializer(data=self.valid_data)
#
#     def test_serializer_valid(self):
#         """Тестирование валидности сериализатора узла сети."""
#         self.assertTrue(self.serializer.is_valid())
#
#     def test_serializer_invalid_email(self):
#         """Тестирование сериализатора с неуникальным email."""
#         # Создание узла с тем же email
#         NetworkNode.objects.create(
#             name="Другой узел",
#             email="test@example.com",
#             country="Россия",
#             city="Ростов на дону",
#             street="Другая улица",
#             house_number="2",
#             product=self.product,
#             product_name="Другой продукт",
#             product_model="AP-200",
#             supplier=self.supplier,
#             level=1,
#         )
#         self.serializer = NetworkNodeSerializer(data=self.valid_data)
#         self.assertFalse(self.serializer.is_valid())
#         self.assertIn("email", self.serializer.errors)
#
#     def test_serializer_invalid_product(self):
#         """Тестирование сериализатора с несуществующим продуктом."""
#         invalid_data = self.valid_data.copy()
#         invalid_data["product"] = 999  # Не существующий продукт
#         self.serializer = NetworkNodeSerializer(data=invalid_data)
#         self.assertFalse(self.serializer.is_valid())
#         self.assertIn(
#             "product", self.serializer.errors
#         )  # Проверка на наличие ошибки для поля product
#         self.assertEqual(
#             self.serializer.errors["product"][0].code, "does_not_exist"
#         )  # Проверка кода ошибки
#
#     def test_serializer_invalid_supplier(self):
#         """Тестирование сериализатора с несуществующим поставщиком."""
#         invalid_data = self.valid_data.copy()
#         invalid_data["supplier"] = 999  # Не существующий поставщик
#         self.serializer = NetworkNodeSerializer(data=invalid_data)
#         self.assertFalse(self.serializer.is_valid())
#         self.assertIn(
#             "supplier", self.serializer.errors
#         )  # Проверка на наличие ошибки для поля supplier
#         self.assertEqual(
#             self.serializer.errors["supplier"][0].code, "does_not_exist"
#         )  # Проверка кода ошибки
#
#
# class PaymentSerializerTest(TestCase):
#     def setUp(self):
#         """Создание тестовых данных для платежа."""
#         self.supplier = Supplier.objects.create(name="Тестовый поставщик")
#         self.product = Product.objects.create(
#             name="Тестовый продукт", model="TP-100", release_date="2025-01-01"
#         )
#         self.network_node = NetworkNode.objects.create(
#             name="Тестовый узел",
#             email="test@example.com",
#             country="Россия",
#             city="Ростов на дону",
#             street="Тестовая улица",
#             house_number="1",
#             product=self.product,
#             product_name="Тестовый продукт",
#             product_model="TP-100",
#             supplier=self.supplier,
#             level=0,
#         )
#         self.valid_data = {
#             "supplier": self.supplier.id,
#             "network_node": self.network_node.id,
#             "amount": 100.00,
#             "description": "Тестовый платеж",
#         }
#         self.serializer = PaymentSerializer(data=self.valid_data)
#
#     def test_serializer_valid(self):
#         """Тестирование валидности сериализатора платежа."""
#         self.assertTrue(self.serializer.is_valid())
#
#     def test_serializer_invalid_missing_amount(self):
#         """Тестирование сериализатора с отсутствующей суммой платежа."""
#         invalid_data = self.valid_data.copy()
#         invalid_data["amount"] = None  # Отсутствие суммы
#         self.serializer = PaymentSerializer(data=invalid_data)
#         self.assertFalse(self.serializer.is_valid())
#         self.assertIn("amount", self.serializer.errors)
#
#     def test_serializer_invalid_missing_supplier(self):
#         """Тестирование сериализатора с отсутствующим поставщиком."""
#         invalid_data = self.valid_data.copy()
#         invalid_data["supplier"] = None  # Отсутствие поставщика
#         self.serializer = PaymentSerializer(data=invalid_data)
#         self.assertFalse(self.serializer.is_valid())
#         self.assertIn("supplier", self.serializer.errors)
#
#     def test_serializer_invalid_missing_network_node(self):
#         """Тестирование сериализатора с отсутствующим узлом сети."""
#         invalid_data = self.valid_data.copy()
#         invalid_data["network_node"] = None  # Отсутствие узла сети
#         self.serializer = PaymentSerializer(data=invalid_data)
#         self.assertFalse(self.serializer.is_valid())
#         self.assertIn("network_node", self.serializer.errors)
