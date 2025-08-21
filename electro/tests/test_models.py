# from decimal import Decimal
#
# from django.test import TestCase
#
# from electro.models import NetworkNode, Payment, Product, Supplier
#
#
# class SupplierModelTest(TestCase):
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
#     def test_supplier_str(self):
#         """Тестирование строкового представления поставщика."""
#         self.assertEqual(str(self.supplier), "Поставщик")
#
#     def test_update_debt(self):
#         """Тестирование обновления задолженности поставщика."""
#         self.supplier.update_debt(Decimal("50.00"))
#         self.assertEqual(self.supplier.debt, Decimal("50.00"))
#
#     def test_update_debt_exceeding_amount(self):
#         """Тестирование обновления задолженности с превышением допустимой суммы."""
#         with self.assertRaises(ValueError):
#             self.supplier.update_debt(
#                 Decimal("150.00")
#             )  # Проверка на превышение задолженности
#
#     def test_initial_debt(self):
#         """Тестирование начальной задолженности поставщика."""
#         self.assertEqual(self.supplier.debt, Decimal("100.00"))
#
#     def test_debt_not_negative(self):
#         """Тестирование, чтобы задолженность не была отрицательной."""
#         self.supplier.update_debt(Decimal("100.00"))
#         self.assertEqual(self.supplier.debt, Decimal("0.00"))
#
#
# class ProductModelTest(TestCase):
#     def setUp(self):
#         """Создание тестовых данных для продукта."""
#         self.product = Product.objects.create(
#             name="Тестовый продукт", model="TP-100", release_date="2025-01-01"
#         )
#
#     def test_str_method(self):
#         """Тестирование строкового представления продукта."""
#         self.assertEqual(str(self.product), "Тестовый продукт")
#
#     def test_product_creation(self):
#         """Тестирование создания продукта."""
#         self.assertEqual(Product.objects.count(), 1)
#         self.assertEqual(self.product.name, "Тестовый продукт")
#         self.assertEqual(self.product.model, "TP-100")
#
#
# class NetworkNodeModelTest(TestCase):
#     def setUp(self):
#         """Создание тестовых данных для узла сети."""
#         self.supplier = Supplier.objects.create(name="Тестовый поставщик")
#         self.product = Product.objects.create(
#             name="Тестовый продукт", release_date="2025-01-01"
#         )
#         self.node = NetworkNode.objects.create(
#             name="Тестовый узел",
#             email="test@example.com",
#             country="Россия",
#             city="Ростов на дону",
#             street="Тестовая улица",
#             house_number="1",
#             product=self.product,
#             product_name="Тестовый продукт",
#             product_model="TP-100",
#             product_release_date="2025-01-01",
#             supplier=self.supplier,
#             debt=100.00,
#             level=0,
#         )
#
#     def test_str_method(self):
#         """Тестирование строкового представления узла сети."""
#         self.assertEqual(str(self.node), "Тестовый узел")
#
#     def test_node_creation(self):
#         """Тестирование создания узла сети."""
#         self.assertEqual(NetworkNode.objects.count(), 1)
#         self.assertEqual(self.node.email, "test@example.com")
#
#     def test_default_debt(self):
#         """Тестирование начальной задолженности для нового узла сети."""
#         node = NetworkNode.objects.create(
#             name="Другой узел",
#             email="another@example.com",
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
#         self.assertEqual(node.debt, 0.00)
#
#
# class PaymentModelTest(TestCase):
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
#             product=self.product,  # Указываем продукт
#             product_name="Тестовый продукт",
#             product_model="TP-100",
#             supplier=self.supplier,
#             level=0,
#         )
#
#         self.payment = Payment.objects.create(
#             supplier=self.supplier, network_node=self.network_node, amount=100.00
#         )
#
#     def test_str_method(self):
#         """Тестирование строкового представления платежа."""
#         self.assertEqual(
#             str(self.payment),
#             f"Платеж на сумму {self.payment.amount} от {self.payment.payment_date.strftime('%Y-%m-%d')}",
#         )
#
#     def test_payment_creation(self):
#         """Тестирование создания платежа."""
#         self.assertEqual(Payment.objects.count(), 1)
#         self.assertEqual(self.payment.amount, 100.00)
#         self.assertEqual(self.payment.supplier, self.supplier)
#         self.assertEqual(self.payment.network_node, self.network_node)
