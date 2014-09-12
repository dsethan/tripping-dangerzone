from django.contrib import admin
from checkout.models import CustomerProfile

class CustomerProfileAdmin(admin.ModelAdmin):
	list_display = ('customer_id',)

admin.site.register(CustomerProfile, CustomerProfileAdmin)
# Register your models here.
