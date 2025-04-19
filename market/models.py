from django.db import models

from accounts.models import CustomUser

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name


# SubCategory Model
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


# Seller Model
class Seller(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='stores', null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00) 
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='vendors_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/seller/{self.id}/"





# # ProductView Model (for tracking user views)
# class ProductView(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='views', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='views', on_delete=models.CASCADE)
#     viewed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} viewed {self.product.name}'


# # Purchase Model (for tracking purchases)
# class Purchase(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='purchases', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='purchases', on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     purchased_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} purchased {self.product.name} ({self.quantity} items)'


# # Order Model (to track user orders)
# class Order(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     order_status = models.CharField(max_length=50, choices=[
#         ('pending', 'Pending'),
#         ('shipped', 'Shipped'),
#         ('delivered', 'Delivered'),
#         ('cancelled', 'Cancelled')
#     ], default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"


# # Cart Model (for shopping cart functionality)
# class Cart(models.Model):
#     user = models.OneToOneField(CustomUser, related_name='cart', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Cart of {self.user.username}"


# # CartItem Model (to store items in the shopping cart)
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name} in cart"


# # Address Model (for saving user's address information)
# class Address(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='addresses', on_delete=models.CASCADE)
#     street_address = models.CharField(max_length=255)
#     city = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=20)
#     country = models.CharField(max_length=100)
#     is_primary = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username}'s Address"


# # Review Model (for product reviews by users)
# class Review(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
#     rating = models.DecimalField(max_digits=2, decimal_places=1, choices=[
#         (1, '1 Star'),
#         (2, '2 Stars'),
#         (3, '3 Stars'),
#         (4, '4 Stars'),
#         (5, '5 Stars')
#     ])
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Review of {self.product.name} by {self.user.username}"


# # Payment Model (to store payment details for orders)
# class Payment(models.Model):
#     order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
#     payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
#     payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     paid_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Payment for {self.order.id} by {self.order.user.username}"






class CategorySuppliments(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Suppliment(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categorySuppliments = models.ForeignKey(CategorySuppliments, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    seller = models.ForeignKey(Seller, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    suppliments = models.ManyToManyField(Suppliment, related_name='products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/product/{self.id}/"


class Order(models.Model):
    RECEIVED = 'Received'
    IN_PROGRESS = 'In Progress'
    IN_TRANSIT = 'In Transit'
    COMPLETE = 'Complete'
    CANCELLED = 'Cancelled'
    CONFIRMED = 'Confirmed'

    STATUS_CHOICES = [
        (RECEIVED, 'Received'),
        (IN_PROGRESS, 'In Progress'),
        (IN_TRANSIT, 'In Transit'),
        (COMPLETE, 'Complete'),
        (CANCELLED, 'Cancelled'),
        (CONFIRMED, 'Confirmed'),
    ]

    location = models.CharField(max_length=255, blank=True, null=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=RECEIVED)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    suppliments = models.ManyToManyField(Suppliment, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} from {self.store.name if self.store else 'Unknown'}"
    


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"