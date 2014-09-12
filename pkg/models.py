from django.db import models
from item.models import Item
from orders.models import Order
from users.models import UserProfile


class Cart(models.Model):
	profile = models.ForeignKey(UserProfile)
	total = models.IntegerField(default=0) # in cents


class CartItem(models.Model):
	cart = models.ForeignKey(Cart)
	item = models.ForeignKey(Item)
	qty = models.IntegerField(default=1)

# Create your models here.

