from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления пользователями.

    Позволяет выполнять операции CRUD (создание, чтение, обновление, удаление) для модели CustomUser.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
