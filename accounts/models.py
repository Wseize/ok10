from django.contrib.auth.models import AbstractUser
from django.db import models


TUNISIAN_GOVERNORATES = [
    ('Ariana', 'Ariana'),
    ('Beja', 'Beja'),
    ('Ben Arous', 'Ben Arous'),
    ('Bizerte', 'Bizerte'),
    ('Gabes', 'Gabes'),
    ('Gafsa', 'Gafsa'),
    ('Jendouba', 'Jendouba'),
    ('Kairouan', 'Kairouan'),
    ('Kasserine', 'Kasserine'),
    ('Kebili', 'Kebili'),
    ('Kef', 'Kef'),
    ('Mahdia', 'Mahdia'),
    ('Manouba', 'Manouba'),
    ('Medenine', 'Medenine'),
    ('Monastir', 'Monastir'),
    ('Nabeul', 'Nabeul'),
    ('Sfax', 'Sfax'),
    ('Sidi Bouzid', 'Sidi Bouzid'),
    ('Siliana', 'Siliana'),
    ('Sousse', 'Sousse'),
    ('Tataouine', 'Tataouine'),
    ('Tozeur', 'Tozeur'),
    ('Tunis', 'Tunis'),
    ('Zaghouan', 'Zaghouan'),
]

class CustomUser(AbstractUser):
    username_field = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=50, choices=TUNISIAN_GOVERNORATES, null=True, blank=True, default='Tunis',)
    favorites = models.ManyToManyField('market.Product', related_name='favorited_by', blank=True)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username



# # models.py
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# import uuid

# TUNISIAN_GOVERNORATES = [
#     ('Ariana', 'Ariana'), ('Beja', 'Beja'), ('Ben Arous', 'Ben Arous'),
#     ('Bizerte', 'Bizerte'), ('Gabes', 'Gabes'), ('Gafsa', 'Gafsa'),
#     ('Jendouba', 'Jendouba'), ('Kairouan', 'Kairouan'), ('Kasserine', 'Kasserine'),
#     ('Kebili', 'Kebili'), ('Kef', 'Kef'), ('Mahdia', 'Mahdia'),
#     ('Manouba', 'Manouba'), ('Medenine', 'Medenine'), ('Monastir', 'Monastir'),
#     ('Nabeul', 'Nabeul'), ('Sfax', 'Sfax'), ('Sidi Bouzid', 'Sidi Bouzid'),
#     ('Siliana', 'Siliana'), ('Sousse', 'Sousse'), ('Tataouine', 'Tataouine'),
#     ('Tozeur', 'Tozeur'), ('Tunis', 'Tunis'), ('Zaghouan', 'Zaghouan'),
# ]

# class CustomUser(AbstractUser):
#     username_field = models.CharField(max_length=255, null=True, blank=True)
#     mobile = models.CharField(max_length=12, null=True, blank=True)
#     address = models.CharField(max_length=50, choices=TUNISIAN_GOVERNORATES, null=True, blank=True, default='Tunis')
#     favorites = models.ManyToManyField('market.Product', related_name='favorited_by', blank=True)

#     referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
#     referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')

#     is_first_time = models.BooleanField(default=True)

#     def save(self, *args, **kwargs):
#         if not self.referral_code:
#             self.referral_code = str(uuid.uuid4())[:8].upper()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.username

# class Wallet(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     points = models.IntegerField(default=0)

#     def __str__(self):
#         return f"Wallet of {self.user.username}"

# class PointTransaction(models.Model):
#     wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
#     change = models.IntegerField()
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.change} points at {self.created_at}"