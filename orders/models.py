from django.db import models
from users.models import User, UserProfile
from item.models import Item
from cal.models import Entry
from drivers.models import DriverProfile
from restaurants.models import Restaurant
import datetime
from datetime import date, time, timedelta
import datetime

class Order(models.Model):
	
	PENDING = 'PDG'
	DELIVERY = 'OUT'
	DELIVERED = 'DVD'

	STATUS = (
		(PENDING, 'PDG'),
		(DELIVERY, 'OUT'),
		(DELIVERED, 'DVD'),
		)

	user_profile = models.ForeignKey(UserProfile)
	#driver = models.ForeignKey(DriverProfile)
	restaurant = models.ForeignKey(Restaurant)

	total = models.IntegerField(default=0) # in cents
	entry = models.ForeignKey(Entry)
	status = models.CharField(max_length=3, choices=STATUS, default=PENDING)

	date_in = models.DateField(auto_now=True)
	time_in = models.TimeField(auto_now=True)

	date_out = models.DateField(auto_now=True)
	time_out = models.DateField(auto_now=True)

	order_success = models.BooleanField(default=False)

	order_rating = models.IntegerField(default=0)

	def __unicode__(self):
		return self.status

	def view_order_total_in_usd(self):
		self_str = str(self.total)
		cents = self_str[-2:]
		dollars = self_str[:-2]
		return "$" + dollars + "." + cents


class OrderItem(models.Model):
	item = models.ForeignKey(Item)
	order = models.ForeignKey(Order)
	quantity = models.IntegerField(default=0)
