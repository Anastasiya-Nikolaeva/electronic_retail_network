from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (NetworkNodeViewSet, PaymentViewSet, ProductViewSet,
                    SupplierViewSet)

app_name = "electro"

router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet)
router.register(r"network-nodes", NetworkNodeViewSet)
router.register(r"products", ProductViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
