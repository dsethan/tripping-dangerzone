from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant
from datetime import date, time, timedelta
from googlemaps import GoogleMaps

class UserProfile(models.Model):
	# Basic registration data
	North_Carolina = 'NC'
	STATES = (
		(North_Carolina, 'NC'),
		)
	user = models.OneToOneField(User)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=2, choices=STATES)
	phone = models.CharField(max_length=12)
	# Information about associated restaurant
	restaurant = models.ForeignKey(Restaurant)
	# Data fields
	logins = models.IntegerField(default=0)
	clicks = models.IntegerField(default=0)
	total_orders = models.IntegerField(default=0) 
	total_spent = models.IntegerField(default=0) # in cents
	last_click = models.DateField(auto_now=True)
	last_login = models.DateField(auto_now=True)
	avg_delivery_time = models.IntegerField(default=0) # in seconds
	avg_rating = models.IntegerField(default=0) # in stars


	def get_directions(self):
		api_key = "AIzaSyAUYyU_aUoW5iu_pZZ30U0V_bfdPHQMBQM"
		gmaps = GoogleMaps(api_key)
		addr_string = str(self.address) + " " + str(self.city) + " " + str(self.state)
		restaurant_addr = str(self.restaurant.address1) + " " + str(self.restaurant.city) + " " + str(self.restaurant.state)
		dirs = gmaps.directions(restaurant_addr, addr_string)
		time = dirs['Directions']['Duration']['seconds']
		mins = time/60
		secs = time%60
		time_reformatted = str(mins)+":"+str(secs)
		dist = dirs['Directions']['Distance']['meters']
		in_miles = float(dist*.000621371)
		in_miles_reformatted = str(in_miles)
		return (time_reformatted, in_miles_reformatted)

	def increase_logins(self):
		self.logins = self.logins + 1

	def increase_clicks(self):
		self.clicks = self.clicks + 1

	def __unicode__(self):
		return self.id