from django.shortcuts import render
from orders.models import Order
from drivers.models import DriverProfile
from users.models import User

def dispatch_route(request):
	context = RequestContext(request)
	user = request.user
	