from django.contrib import admin
from users.models import UserProfile
from django.contrib.auth.models import User

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'address', 'city', 'state', 'restaurant', 'logins', 'clicks', 'total_orders', 'total_spent', 'last_click', 'last_login', 'avg_delivery_time', 'avg_rating')

admin.site.register(UserProfile, UserProfileAdmin)
# Register your models here.
