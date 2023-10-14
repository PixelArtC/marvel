from django.contrib import admin
from .models import NFT, UserProfile, PrivateKey

@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'volume', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display =  ['user', 'email', 'full_name', 'wallet_address', 'balance', 'private_key']

@admin.register(PrivateKey)
class PrivateKeyAdmin(admin.ModelAdmin):
    list_display = ['key']

# Register your models here.
