from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategorySupplimentViewSet, CategoryViewSet, OrderProductViewSet, OrderViewSet, ProductImageViewSet, SubCategoryViewSet, SellerViewSet, ProductViewSet, SupplimentViewSet,
)
from market import views

# Create a router and register the viewsets with it
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'sellers', SellerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-products', OrderProductViewSet, basename='order-products')
router.register('product-gallery', ProductImageViewSet)
router.register(r'suppliments', SupplimentViewSet)
router.register(r'category-suppliments', CategorySupplimentViewSet)
# router.register(r'purchases', PurchaseViewSet)
# router.register(r'orders', OrderViewSet)
# router.register(r'carts', CartViewSet)
# router.register(r'cart-items', CartItemViewSet)
# router.register(r'addresses', AddressViewSet)
# router.register(r'reviews', ReviewViewSet)
# router.register(r'payments', PaymentViewSet)

# Include the router URLs in the Django URL patterns
urlpatterns = [
    path('search/', views.search, name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
] + router.urls
