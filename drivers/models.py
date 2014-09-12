from django.db import models
from users.models import User
from restaurants.models import Restaurant
from datetime import date, time, timedelta

class DriverProfile(models.Model):
	# Basic registration data
	North_Carolina = 'NC'
	STATES = (
		(North_Carolina, 'NC'),
	)
	user = models.ForeignKey(User)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2, choices=STATES)

	# Information about associated restaurant
	restaurant = models.ForeignKey(Restaurant)

	# Data fields
	total_deliveries = models.IntegerField(default=0)
	avg_delivery_time = models.IntegerField(default=0)
	avg_rating = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.first_name + " " + self.user.last_name