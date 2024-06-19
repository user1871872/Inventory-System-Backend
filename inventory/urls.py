from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, sales_statistics,purchase_product,list_purchases,get_sales_statistics,SaleStatisticViewSet,PurchaseViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'sales-statistics', SaleStatisticViewSet)
router.register(r'purchases', PurchaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sales-statistics/', sales_statistics, name='sales-statistics'),
    path('purchase/', purchase_product, name='purchase_product'),
    path('purchases/', list_purchases, name='list_purchases'),
    path('sales-statistics/', get_sales_statistics, name='get_sales_statistics'),
]
