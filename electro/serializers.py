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
        if Supplier.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
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
        Проверяет существование связанных объектов (продукта и поставщика).

        :param attrs: Атрибуты, переданные для валидации.
        :raises serializers.ValidationError: Если указанный продукт или поставщик не существует.
        :return: Проверенные атрибуты.
        """
        # Проверка на существование продукта
        if "product" in attrs:
            try:
                Product.objects.get(id=attrs["product"].id)
            except Product.DoesNotExist:
                raise serializers.ValidationError("Указанный продукт не существует.")

            # Проверка на существование поставщика
        if "supplier" in attrs:
            try:
                Supplier.objects.get(id=attrs["supplier"].id)
            except Supplier.DoesNotExist:
                raise serializers.ValidationError("Указанный поставщик не существует.")

        return attrs


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Преобразует объекты модели Product в JSON и обратно.
    Необходима валидация данных, если это требуется.
    """

    class Meta:
        model = Product
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.

    Преобразует объекты модели Payment в JSON и обратно.
    Необходима валидация данных, если это требуется.
    """

    class Meta:
        model = Payment
        fields = "__all__"
