from django.utils import timezone
from rest_framework import serializers

from .models import NetworkNode, Payment, Product, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Supplier.

    Преобразует объекты модели Supplier в JSON и обратно.
    Обеспечивает валидацию данных, включая проверку уникальности email.
    Поле 'debt' доступно только для чтения.
    """

    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ["debt"]

    def validate_email(self, value):
        """
        Проверяет, существует ли уже поставщик с указанным email.

        :param value: Email для проверки.
        :raises serializers.ValidationError: Если email уже используется.
        :return: Проверенный email.
        """
        if self.instance is None:  # Проверяем, если это новый объект
            if Supplier.objects.filter(email=value).exists():
                raise serializers.ValidationError("Этот email уже используется.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Преобразует объекты модели Product в JSON и обратно.
    Необходима валидация данных, если это требуется.
    """

    class Meta:
        model = Product
        fields = "__all__"

    def validate_release_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Дата выпуска не может быть в будущем.")
        return value


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkNode.

    Преобразует объекты модели NetworkNode в JSON и обратно.
    Обеспечивает валидацию данных, включая проверку уникальности email,
    а также проверку существования связанных объектов (продукта и поставщика).
    """

    class Meta:
        model = NetworkNode
        fields = "__all__"

    def validate_email(self, value):
        """
        Проверяет, существует ли уже узел сети с указанным email.

        :param value: Email для проверки.
        :raises serializers.ValidationError: Если email уже используется.
        :return: Проверенный email.
        """
        if NetworkNode.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value

    def validate(self, attrs):
        """
        Проверяет существование связанных объектов (продукта и поставщика),
        а также наличие обязательных полей.

        :param attrs: Атрибуты, переданные для валидации.
        :raises serializers.ValidationError: Если указанный продукт или поставщик не существует,
                                              или если отсутствует product_release_date.
        :return: Проверенные атрибуты.
        """
        # Проверка на существование продукта
        if "product" in attrs:
            try:
                product = Product.objects.get(id=attrs["product"].id)
                attrs["product_release_date"] = product.release_date
            except Product.DoesNotExist:
                raise serializers.ValidationError("Указанный продукт не существует.")

        # Проверка на существование поставщика
        if "supplier" in attrs:
            try:
                Supplier.objects.get(id=attrs["supplier"].id)
            except Supplier.DoesNotExist:
                raise serializers.ValidationError("Указанный поставщик не существует.")

        return attrs


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.

    Преобразует объекты модели Payment в JSON и обратно.
    Необходима валидация данных, если это требуется.
    """

    class Meta:
        model = Payment
        fields = "__all__"

    def validate(self, attrs):
        if "supplier" not in attrs or attrs["supplier"] is None:
            raise serializers.ValidationError({"supplier": "Это поле обязательно."})
        if "network_node" not in attrs or attrs["network_node"] is None:
            raise serializers.ValidationError({"network_node": "Это поле обязательно."})
        return attrs
