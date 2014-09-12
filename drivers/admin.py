from django.contrib import admin
from drivers.models import DriverProfile
# Register your models here.

class DriverProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'city', 'state', 'restaurant', 'total_deliveries', 'avg_delivery_time', 'avg_rating')

admin.site.register(DriverProfile, DriverProfileAdmin)


