from django.contrib import admin
from item.models import Item
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'cost', 'description', 'prep_category', 'number_ordered', 'total_spent', 'available')

admin.site.register(Item, ItemAdmin)