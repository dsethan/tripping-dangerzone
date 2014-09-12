from django.db import models
from orders.models import Order
from drivers.models import DriverProfile
# Create your models here.

class Dispatch(models.Model):
	date = models.DateField(auto_now=False)
	start_time = models.TimeField(auto_now=False)
	length = models.IntegerField(default=20) # in minutes
	driver = models.ForeignKey(DriverProfile)

class DispatchOrder(models.Model):
	order = models.ForeignKey(Order)
	dispatch = models.ForeignKey(Dispatch)