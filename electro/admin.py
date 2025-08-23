from django.contrib import admin

from .models import NetworkNode, Payment, Product, Supplier


class BaseAdmin(admin.ModelAdmin):
    """Базовый класс для админ-панелей, если потребуется общая функциональность."""

    pass


class SupplierAdmin(BaseAdmin):
    """Админ-панель для управления поставщиками."""

    list_display = ("name", "email", "country", "city", "debt", "created_at")
    search_fields = ("name", "email")


class NetworkNodeAdmin(BaseAdmin):
    """Админ-панель для управления сетевыми узлами."""

    list_display = ("name", "city", "supplier", "debt", "created_at")
    list_filter = ("city", "debt")
    actions = ["clear_debt"]

    def clear_debt(self, request, queryset):
        """Очистить задолженность для выбранных сетевых узлов."""
        updated_count = queryset.update(debt=0)
        self.message_user(
            request, f"Задолженность успешно очищена у {updated_count} объектов."
        )

    clear_debt.short_description = "Очистить задолженность перед поставщиком"


class ProductAdmin(BaseAdmin):
    """Админ-панель для управления продуктами."""

    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")


class PaymentAdmin(BaseAdmin):
    """Админ-панель для управления платежами."""

    list_display = ("supplier", "network_node", "amount", "payment_date", "description")
    list_filter = ("supplier", "network_node", "payment_date")
    search_fields = ("description",)


# Регистрация моделей в админ-панели
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(NetworkNode, NetworkNodeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Payment, PaymentAdmin)
