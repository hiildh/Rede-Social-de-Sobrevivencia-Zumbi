from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurvivorViewSet, InventoryViewSet, register_survivor, current_survivor, reports, survivor_inventory, get_survivor_by_name

router = DefaultRouter()
router.register(r'survivors', SurvivorViewSet, basename='survivor')
router.register(r'inventories', InventoryViewSet, basename='inventory')

urlpatterns = [
    path('register-survivor/', register_survivor, name='register-survivor'),
    path('survivors/current/', current_survivor, name='current-survivor'),
    path('survivors/inventory/<int:survivor_id>/', survivor_inventory, name='survivor-inventory'),
    path('survivors/get-by-name/', get_survivor_by_name, name='get-survivor-by-name'),
    path('reports/', reports, name='reports'),
    path('api/', include(router.urls)),
]
