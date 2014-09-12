from django.contrib import admin
from pkg.models import CartItem, Cart

class CartItemAdmin(admin.ModelAdmin):
	list_display = ('cart', 'item', 'qty')

class CartAdmin(admin.ModelAdmin):
	list_display = ('profile', 'total')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
# Register your models here.
