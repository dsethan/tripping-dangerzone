from django.db import models
from drivers.models import DriverProfile
from cal.models import Entry
from orders.models import Order
from dispatch.models import Dispatch, DispatchOrder

class DriverDispatchLink(models.Model):
	dispatch = models.ForeignKey(Dispatch)
	driver = models.ForeignKey(DriverProfile)