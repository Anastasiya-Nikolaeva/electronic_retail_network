from django.db import models


class Supplier(models.Model):
    """
    Модель поставщика.

    Хранит информацию о поставщике, включая его имя, контактные данные и задолженность.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_debt(self, amount):
        """
        Обновляет задолженность поставщика.

        :param amount: Сумма, на которую уменьшается задолженность.
        """
        if amount > self.debt:
            raise ValueError(
                "Сумма уменьшения задолженности превышает текущую задолженность."
            )
        self.debt -= amount
        self.save()

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель продукта.

    Хранит информацию о продукте, включая его название, модель и дату выпуска.
    """

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return self.name


class NetworkNode(models.Model):
    """
    Модель узла сети.

    Хранит информацию о сетевых узлах, включая их уровень, контактные данные и связанные продукты.
    """

    LEVEL_CHOICES = [
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="nodes")
    product_name = models.CharField(max_length=255)
    product_model = models.CharField(max_length=255)
    product_release_date = models.DateField(null=True, blank=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="nodes"
    )
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    level = models.IntegerField(choices=LEVEL_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    """
    Модель платежа.

    Хранит информацию о платежах, включая сумму, дату и связанные узлы сети и поставщиков.
    """

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True,
    )
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Платеж на сумму {self.amount} от {self.payment_date.strftime('%Y-%m-%d')}"
