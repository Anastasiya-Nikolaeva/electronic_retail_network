from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ только активным пользователям.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь доступ к представлению.

        Параметры:
        request (Request): Запрос, который содержит информацию о пользователе.
        view (View): Представление, к которому осуществляется доступ.

        Возвращает:
        bool: True, если доступ разрешен, иначе False.
        """
        return request.user.is_authenticated and request.user.is_active
