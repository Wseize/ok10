from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView,LogoutView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from accounts.serializers import CustomUserSerializer
from market.permissions import IsSuperUserOrSelf
from .models import CustomUser



# Create your views here.

class CustomRegisterView(RegisterView):
    pass


class CustomVerifyEmailView(VerifyEmailView):
    pass


class CustomLoginView(LoginView):
    pass
   


class CustomLogoutView(LogoutView):
    pass


class CustomPasswordChangeView(PasswordChangeView):
    pass


class CustomPasswordResetView(PasswordResetView):
    pass

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    pass

from market.serializers import ProductSerializer
from market.models import Product
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

# class UserProfileView(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

#     @action(detail=True, methods=['post'])
#     def add_favorite(self, request, pk=None):
#         user = self.get_object()  # Get the current user object
#         product_id = request.data.get('product_id')

#         if not product_id:
#             return Response({"error": "Product ID is required."}, status=400)

#         try:
#             product_id = int(product_id)  # Convert product_id to integer
#             product = Product.objects.get(id=product_id)
#         except (Product.DoesNotExist, ValueError):
#             return Response({"error": "Product not found or invalid product ID."}, status=404)

#         # Add the product to user's favorites
#         user.favorites.add(product)
#         user.save()

#         return Response({"message": "Product added to favorites."})

#     @action(detail=True, methods=['post'])
#     def remove_favorite(self, request, pk=None):
#         user = self.get_object()
#         product_id = request.data.get('product_id')

#         if not product_id:
#             return Response({"error": "Product ID is required."}, status=400)

#         try:
#             product_id = int(product_id)  # Convert product_id to integer
#             product = Product.objects.get(id=product_id)
#         except (Product.DoesNotExist, ValueError):
#             return Response({"error": "Product not found or invalid product ID."}, status=404)

#         # Remove the product from user's favorites
#         user.favorites.remove(product)
#         user.save()

#         return Response({"message": "Product removed from favorites."})

#     @action(detail=True, methods=['get'])
#     def favorites(self, request, pk=None):
#         user = self.get_object()
#         favorites = user.favorites.all()
#         serializer = ProductSerializer(favorites, many=True)
#         return Response(serializer.data)


class UserProfileView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsSuperUserOrSelf]

    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        user = self.get_object()  # Get the current user object
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)

        try:
            product_id = int(product_id)  # Convert product_id to integer
            product = Product.objects.get(id=product_id)
        except (Product.DoesNotExist, ValueError):
            return Response({"error": "Product not found or invalid product ID."}, status=404)

        # Add the product to user's favorites
        user.favorites.add(product)
        user.save()

        return Response({"message": "Product added to favorites."})

    @action(detail=True, methods=['post'])
    def remove_favorite(self, request, pk=None):
        user = self.get_object()
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)

        try:
            product_id = int(product_id)  # Convert product_id to integer
            product = Product.objects.get(id=product_id)
        except (Product.DoesNotExist, ValueError):
            return Response({"error": "Product not found or invalid product ID."}, status=404)

        # Remove the product from user's favorites
        user.favorites.remove(product)
        user.save()

        return Response({"message": "Product removed from favorites."})

    @action(detail=True, methods=['get'])
    def favorites(self, request, pk=None):
        user = self.get_object()
        favorites = user.favorites.all()
        serializer = ProductSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_seller_status(self, request, pk=None):
        user = self.get_object()
        user.is_seller = not user.is_seller  # Toggle the seller status
        user.save()

        return Response({"message": f"Seller status updated to {user.is_seller}"})

    @action(detail=True, methods=['post'])
    def toggle_admin_status(self, request, pk=None):
        user = self.get_object()
        user.is_admin = not user.is_admin  # Toggle the admin status
        user.save()

        return Response({"message": f"Admin status updated to {user.is_admin}"})
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from .models import Wallet, PointTransaction, CustomUser
# from .serializers import WalletSerializer, PointTransactionSerializer, TransferPointsSerializer

# class WalletViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     def list(self, request):
#         user = request.user
#         wallet, created = Wallet.objects.get_or_create(user=user)
#         response_data = {
#             "points": wallet.points,
#             "referral_code": user.referral_code,
#             "is_first_time": user.is_first_time,
#         }

#         if created:
#             # Assign initial points
#             wallet.points = 50
#             wallet.save()

#             PointTransaction.objects.create(
#                 wallet=wallet,
#                 change=50,
#                 description="Initial 50 SPD points assigned"
#             )

#             # Auto referral reward if referred_by is already set
#             if user.referred_by:
#                 inviter = user.referred_by
#                 inviter_wallet, _ = Wallet.objects.get_or_create(user=inviter)
#                 inviter_wallet.points += 40
#                 inviter_wallet.save()

#                 PointTransaction.objects.create(
#                     wallet=inviter_wallet,
#                     change=40,
#                     description=f"Referral reward for inviting {user.username}"
#                 )

#                 response_data["invited_by"] = inviter.username
#                 response_data["inviter_referral_code"] = inviter.referral_code
#             else:
#                 response_data["invited_by"] = None
#                 response_data["inviter_referral_code"] = None

#             # First-time logic ends here
#             user.is_first_time = False
#             user.save()
#         else:
#             if user.referred_by:
#                 inviter = user.referred_by
#                 response_data["invited_by"] = inviter.username
#                 response_data["inviter_referral_code"] = inviter.referral_code
#             else:
#                 response_data["invited_by"] = None
#                 response_data["inviter_referral_code"] = None

#         return Response(response_data)

#     @action(detail=False, methods=['post'])
#     def set_referral_code(self, request):
#         user = request.user

#         if not user.is_first_time:
#             return Response(
#                 {"error": "Expired action. Referral code can only be set once as a new user."},
#                 status=400
#             )

#         referral_code = request.data.get("referral_code")
#         if not referral_code:
#             return Response({"error": "Referral code is required."}, status=400)

#         try:
#             inviter = CustomUser.objects.get(referral_code=referral_code)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "Referral code is invalid."}, status=404)

#         if inviter == user:
#             return Response({"error": "You cannot use your own referral code."}, status=400)

#         # Apply referral
#         user.referred_by = inviter
#         user.is_first_time = False
#         user.save()

#         inviter_wallet, _ = Wallet.objects.get_or_create(user=inviter)
#         inviter_wallet.points += 40
#         inviter_wallet.save()

#         PointTransaction.objects.create(
#             wallet=inviter_wallet,
#             change=40,
#             description=f"Referral reward for inviting {user.username}"
#         )

#         return Response({
#             "message": f"Referral code {referral_code} applied successfully.",
#             "invited_by": inviter.username,
#             "inviter_points": inviter_wallet.points,
#         })

#     @action(detail=False, methods=['get'])
#     def transactions(self, request):
#         wallet = Wallet.objects.get(user=request.user)
#         transactions = wallet.transactions.all().order_by('-created_at')
#         serializer = PointTransactionSerializer(transactions, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['post'])
#     def transfer(self, request):
#         serializer = TransferPointsSerializer(data=request.data)
#         if serializer.is_valid():
#             recipient_username = serializer.validated_data['recipient_username']
#             points = serializer.validated_data['points']

#             if request.user.username == recipient_username:
#                 return Response({"error": "You cannot transfer points to yourself."}, status=400)

#             try:
#                 recipient = CustomUser.objects.get(username=recipient_username)
#                 sender_wallet = Wallet.objects.get(user=request.user)
#                 recipient_wallet = Wallet.objects.get(user=recipient)

#                 if sender_wallet.points < points:
#                     return Response({"error": "Not enough points."}, status=400)

#                 sender_wallet.points -= points
#                 sender_wallet.save()
#                 recipient_wallet.points += points
#                 recipient_wallet.save()

#                 PointTransaction.objects.create(
#                     wallet=sender_wallet,
#                     change=-points,
#                     description=f"Sent to {recipient.username}"
#                 )
#                 PointTransaction.objects.create(
#                     wallet=recipient_wallet,
#                     change=points,
#                     description=f"Received from {request.user.username}"
#                 )

#                 return Response({"message": "Points transferred successfully."})
#             except CustomUser.DoesNotExist:
#                 return Response({"error": "Recipient not found."}, status=404)

#         return Response(serializer.errors, status=400)
