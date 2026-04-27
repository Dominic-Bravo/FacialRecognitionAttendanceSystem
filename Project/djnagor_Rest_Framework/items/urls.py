from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminItemViewSet, CategoryViewSet, ItemViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"items", ItemViewSet, basename="item")
router.register(r"admin/items", AdminItemViewSet, basename="admin-item")

urlpatterns = [
    path("", include(router.urls)),
]
