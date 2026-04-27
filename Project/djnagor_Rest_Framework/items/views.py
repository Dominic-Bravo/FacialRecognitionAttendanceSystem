from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdminOrManager

from .models import Category, Item
from .permissions import IsOwner
from .serializers import CategorySerializer, ItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user, category__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AdminItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.select_related("owner", "category").all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

# Create your views here.
