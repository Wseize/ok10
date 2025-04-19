from rest_framework import serializers
from .models import Category, CategorySuppliments, OrderProduct, ProductImage, SubCategory, Seller, Product, Order, Suppliment


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']


# SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'name', 'description', 'image']

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value


# Seller Serializer
class SellerSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Seller
        fields = ['id', 'owner', 'name', 'description', 'rating', 'phone_number', 'email', 'image', 'products']



# # ProductView Serializer
# class ProductViewSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()  # Shows the related user's username
#     product = ProductSerializer()

#     class Meta:
#         model = ProductView
#         fields = ['id', 'user', 'product', 'viewed_at']


# # Purchase Serializer
# class PurchaseSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()  # Shows the related user's username
#     product = ProductSerializer()

#     class Meta:
#         model = Purchase
#         fields = ['id', 'user', 'product', 'quantity', 'total_price', 'purchased_at']

#     def validate_product(self, value):
#         if not Product.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("Product does not exist.")
#         return value


# # Order Serializer
# class OrderSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()  # Shows the related user's username
#     order_status = serializers.ChoiceField(choices=Order._meta.get_field('order_status').choices)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'total_price', 'order_status', 'created_at', 'updated_at']

#     def validate_user(self, value):
#         if not User.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("User does not exist.")
#         return value


# # Cart Serializer
# class CartSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()  # Shows the related user's username

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'created_at', 'updated_at']

#     def validate_user(self, value):
#         if not User.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("User does not exist.")
#         return value


# # Cartproduct Serializer
# class CartproductSerializer(serializers.ModelSerializer):
#     cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
#     product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

#     class Meta:
#         model = Cartproduct
#         fields = ['id', 'cart', 'product', 'quantity', 'added_at']

#     def validate_cart(self, value):
#         if not Cart.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("Cart does not exist.")
#         return value

#     def validate_product(self, value):
#         if not Product.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("Product does not exist.")
#         return value


# # Address Serializer
# class AddressSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()  # Shows the related user's username

#     class Meta:
#         model = Address
#         fields = ['id', 'user', 'street_address', 'city', 'postal_code', 'country', 'is_primary', 'created_at', 'updated_at']

#     def validate_user(self, value):
#         if not User.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("User does not exist.")
#         return value


# # Review Serializer
# class ReviewSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()  # Shows the related user's username
#     product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

#     class Meta:
#         model = Review
#         fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at', 'updated_at']

#     def validate_user(self, value):
#         if not User.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("User does not exist.")
#         return value

#     def validate_product(self, value):
#         if not Product.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("Product does not exist.")
#         return value


# # Payment Serializer
# class PaymentSerializer(serializers.ModelSerializer):
#     order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

#     class Meta:
#         model = Payment
#         fields = ['id', 'order', 'payment_method', 'payment_status', 'amount', 'paid_at']

#     def validate_order(self, value):
#         if not Order.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("Order does not exist.")
#         return value



# class CategorySupplimentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CatSuppliments
#         fields = '__all__'


# class SupplimentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Suppliment
#         fields = '__all__'

class CategorySupplimentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySuppliments
        fields = '__all__'


class SupplimentSerializer(serializers.ModelSerializer):
    categorySuppliments_name = serializers.CharField(source='categorySuppliments.name', read_only=True)
    
    class Meta:
        model = Suppliment
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    suppliments = SupplimentSerializer(many=True, read_only=True)
    suppliment_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Suppliment.objects.all(), write_only=True, source='suppliments'
    )
    gallery = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'seller', 'category', 'subcategory', 'name', 'description', 'price', 'stock_quantity', 'image', 'suppliment_ids', 'suppliments', 'gallery']

    def validate_seller(self, value):
        if not Seller.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Seller does not exist.")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value

    def validate_subcategory(self, value):
        if not SubCategory.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Subcategory does not exist.")
        return value

    def validate(self, data):
        category = data.get('category')
        subcategory = data.get('subcategory')

        if subcategory and category:
            if subcategory.category != category:
                raise serializers.ValidationError({
                    'subcategory': 'Selected subcategory does not belong to the selected category.'
                })

        return data


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_name', 'store_name', 'store', 'quantity', 'suppliments']


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    user_mobile = serializers.CharField(source='user.mobile', read_only=True)
    user_address = serializers.CharField(source='user.address', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'location', 'products', 'status', 'created_at', 'total_price', 'user', 'user_mobile', 'user_address']

    def get_products(self, obj):
        ordered_products = OrderProduct.objects.filter(order=obj)
        product_data = []
        for ordered_product in ordered_products:
            product_data.append({
                'id': ordered_product.product.id,
                'product_name': ordered_product.product.name,
                'quantity': ordered_product.quantity,
                'store_name': ordered_product.store.name if ordered_product.store else "Unknown Store",
            })
        return product_data


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
