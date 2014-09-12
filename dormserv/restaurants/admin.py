from django.contrib import admin
from restaurants.models import Restaurant

class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('name', 'address1', 'address2', 'city', 'state', 'max_radius', 'total_orders', 'total_revenue', 'avg_delivery_time', 'avg_rating')

admin.site.register(Restaurant, RestaurantAdmin)
# Register your models here.
