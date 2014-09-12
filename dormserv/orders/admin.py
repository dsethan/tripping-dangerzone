from django.contrib import admin
from orders.models import Order

class OrderAdmin(admin.ModelAdmin):
	list_display = ('user_profile', 'restaurant', 'total')


admin.site.register(Order, OrderAdmin)

# Register your models here.
