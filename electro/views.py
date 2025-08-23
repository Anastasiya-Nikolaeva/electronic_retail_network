from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from users.permission import IsActiveEmployee

from .filters import NetworkNodeFilter
from .models import NetworkNode, Payment, Product, Supplier
from .serializers import (NetworkNodeSerializer, PaymentSerializer,
                          ProductSerializer, SupplierSerializer)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления поставщиками.

    Позволяет выполнять операции CRUD (создание, чтение, обновление, удаление) для модели Supplier.
    Поле 'debt' доступно только для чтения и не может быть обновлено через API.
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsActiveEmployee]

    def update(self, request, *args, **kwargs):
        """
        Запретить обновление поля 'debt' при обновлении поставщика.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Удаляем поле 'debt' из данных, чтобы оно не обновлялось
        request.data.pop("debt", None)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        # Проверка валидности данных
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=400)

        self.perform_update(serializer)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления продуктами.

    Позволяет выполнять операции CRUD (создание, чтение, обновление, удаление) для модели Product.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]

    def perform_create(self, serializer):
        """
        Дополнительная логика при создании продукта (если необходимо).
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Дополнительная логика при обновлении продукта (если необходимо).
        """
        serializer.save()


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления узлами сети.

    Позволяет выполнять операции CRUD (создание, чтение, обновление, удаление) для модели NetworkNode.
    """

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filterset_class = NetworkNodeFilter

    @action(detail=True, methods=["post"])
    def clear_debt(self, request, pk=None):
        """
        Admin action для очистки задолженности перед поставщиком у выбранного узла сети.
        """
        node = self.get_object()
        if node.debt > 0:
            node.debt = 0.00
            node.save()
            return Response({"status": "Задолженность очищена"})
        return Response({"status": "Задолженность уже равна нулю"}, status=400)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления платежами.

    Позволяет выполнять операции CRUD (создание, чтение, обновление, удаление) для модели Payment.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsActiveEmployee]

    def create(self, request, *args, **kwargs):
        # Валидация суммы платежа
        supplier_id = request.data.get("supplier")
        if supplier_id:
            supplier = Supplier.objects.get(id=supplier_id)
            if request.data["amount"] > supplier.debt:
                return Response(
                    {"error": "Сумма платежа превышает задолженность поставщика."},
                    status=400,
                )
        return super().create(request, *args, **kwargs)
