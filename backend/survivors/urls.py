from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurvivorViewSet, InventoryViewSet

router = DefaultRouter()
router.register(r'survivors', SurvivorViewSet)
router.register(r'inventories', InventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
