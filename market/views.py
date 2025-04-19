from rest_framework import viewsets
from .models import Category, CategorySuppliments, ProductImage, SubCategory, Seller, Product, Order, Suppliment
from .serializers import (
    CategorySerializer, CategorySupplimentsSerializer, ProductImageSerializer, SubCategorySerializer, SellerSerializer, ProductSerializer, SupplimentSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


# SubCategory ViewSet
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsStaffOrReadOnly]


# Seller ViewSet
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsStaffOrReadOnly]

# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly] 


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

# # ProductView (for tracking product views)
# class ProductViewViewSet(viewsets.ModelViewSet):
#     queryset = ProductView.objects.all()
#     serializer_class = ProductViewSerializer
#     permission_classes = [IsOwnerOrReadOnly] 


# # Purchase ViewSet
# class PurchaseViewSet(viewsets.ModelViewSet):
#     queryset = Purchase.objects.all()
#     serializer_class = PurchaseSerializer
#     permission_classes = [IsAuthenticated] 


# # Order ViewSet
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated] 


# # Cart ViewSet
# class CartViewSet(viewsets.ModelViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated] 


# # CartItem ViewSet
# class CartItemViewSet(viewsets.ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated] 


# # Address ViewSet
# class AddressViewSet(viewsets.ModelViewSet):
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer
#     permission_classes = [IsAuthenticated] 


# # Review ViewSet
# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]


# # Payment ViewSet
# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [IsAuthenticated]  # Only authenticated users can make payments



# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product




from django.db.models import Q
from django.shortcuts import render
from .models import Product

def search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'search_results.html', {'products': products, 'query': query})


from django.http import JsonResponse
from .models import Product

def search_suggestions(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:5]  # limit to 5 suggestions
    suggestions = [product.name for product in products]
    return JsonResponse({'suggestions': suggestions})







from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, OrderProduct, Product
from .serializers import OrderSerializer, OrderProductSerializer, OrderStatusSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        product_items = request.data.pop('items', [])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order = serializer.instance

        for item in product_items:
            product_id = item.get('product')
            quantity = item.get('quantity', 1)
            if product_id:
                product = get_object_or_404(Product, pk=product_id)
                store = product.store
                order_product = OrderProduct.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    store=store
                )
                # order_product.suppliments.add(*item.get('suppliments', []))  # if you enable supplements

        headers = self.get_success_headers(serializer.data)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        if 'status' in request.data:
            self.serializer_class = OrderStatusSerializer
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if 'status' in request.data:
            self.serializer_class = OrderStatusSerializer
        return super().update(request, *args, **kwargs)


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

class CategorySupplimentViewSet(viewsets.ModelViewSet):
    queryset = CategorySuppliments.objects.all()
    serializer_class = CategorySupplimentsSerializer

class SupplimentViewSet(viewsets.ModelViewSet):
    queryset = Suppliment.objects.all()
    serializer_class = SupplimentSerializer