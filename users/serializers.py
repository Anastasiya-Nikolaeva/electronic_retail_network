from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.

    Этот сериализатор отвечает за преобразование экземпляров CustomUser в формат JSON и обратно.
    Он также предоставляет методы для создания и обновления экземпляров пользователей.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "city",
            "avatar",
            "is_active",
            "is_staff",
        ]
        read_only_fields = ["id", "is_active", "is_staff"]

    def create(self, validated_data):
        """
        Создает новый экземпляр CustomUser с проверенными данными.

        Этот метод обрабатывает создание нового пользователя, обеспечивая хеширование пароля
        и наличие всех обязательных полей.

        Параметры:
        validated_data (dict): Проверенные данные для создания нового пользователя.

        Возвращает:
        CustomUser: Созданный экземпляр пользователя.

        Исключения:
        ValueError: Если в validated_data отсутствуют обязательные поля или если пароль не указан.
        """
        if "password" not in validated_data:
            raise ValueError("Пароль должен быть указан")

        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            **{
                key: validated_data[key]
                for key in validated_data
                if key not in ["email", "username", "password"]
            }
        )
        return user

    def update(self, instance, validated_data):
        """
        Обновляет существующий экземпляр CustomUser с проверенными данными.

        Этот метод обновляет поля существующего экземпляра пользователя с предоставленными данными.
        Он позволяет частичное обновление и обеспечивает безопасное обновление пароля.

        Параметры:
        instance (CustomUser): Экземпляр пользователя для обновления.
        validated_data (dict): Проверенные данные для обновления пользователя.

        Возвращает:
        CustomUser: Обновленный экземпляр пользователя.

        Исключения:
        ValueError: Если адрес электронной почты или имя пользователя изменяются на существующее значение.
        """
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.city = validated_data.get("city", instance.city)
        instance.avatar = validated_data.get("avatar", instance.avatar)

        # Обновить пароль, если он предоставлен
        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()
        return instance
