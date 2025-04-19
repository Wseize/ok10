from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework import serializers

from market.serializers import ProductSerializer
from .models import CustomUser



class CustomRegisterSerializer(RegisterSerializer):
    pass


class CustomLoginSerializer(LoginSerializer):
    pass


class CustomPasswordResetSerializer(PasswordResetSerializer):
    pass


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    pass


class CustomUserSerializer(serializers.ModelSerializer):
    favorites = ProductSerializer(many=True, required=False)  
    # is_first_time = serializers.BooleanField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'mobile', 'address', 'favorites', 'is_seller', 'is_admin']



# # serializers.py
# from rest_framework import serializers
# from .models import Wallet, PointTransaction, CustomUser

# class WalletSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wallet
#         fields = ['points']

# class PointTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PointTransaction
#         fields = ['id', 'change', 'description', 'created_at']

# class TransferPointsSerializer(serializers.Serializer):
#     recipient_username = serializers.CharField()
#     points = serializers.IntegerField(min_value=1)