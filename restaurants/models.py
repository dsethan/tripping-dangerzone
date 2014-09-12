from django.db import models
from datetime import date, time, timedelta

class Restaurant(models.Model):
	North_Carolina = 'NC'
	STATES = (
		(North_Carolina, 'NC'),
	)
	name = models.CharField(max_length=50)
	address1 = models.CharField(max_length=100)
	address2 = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2, choices=STATES)
	max_radius = models.FloatField()
	total_orders = models.IntegerField(default=0) 
	total_revenue = models.IntegerField(default=0) # in cents
	avg_delivery_time = models.IntegerField(default=0) # in seconds
	avg_rating = models.IntegerField(default=0) # in stars (1-5)

	def get_address(self):
		return self.address1 + " " + self.city + " " + self.state

	def __unicode__(self):
		return self.name