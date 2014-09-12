from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from dispatch.models import Dispatch, DispatchOrder
from drivers.models import DriverProfile
from users.models import User, UserProfile
# Create your views here.

def driver_dash(request):
	context = RequestContext(request)

	# Get associated DriverProfile for the current user.
	user = request.user
	driver = get_driver(user)

	# Initialize a list of all dispatches for the current driver
	dispatches = []

	# Get all dispatches associated with the driver that is logged in.
	for dispatch in Dispatch.objects.all():
		if dispatch.driver == driver:
			dispatches.append(dispatch)

	# Get driver's name to passing through to the template
	first = driver.user.first_name
	last = driver.user.last_name

	dispatch_orders = {}
	for do in DispatchOrder.objects.all():
		for dispatch in dispatches:
			if do.dispatch == dispatch:
				if dispatch not in dispatch_orders.keys():
					dispatch_orders[dispatch] = []
				dispatch_orders[dispatch].append(do)

	




	return render_to_response("driver_home.html", 
		{'driver':driver,
		'first':first,
		'last':last,
		'dispatches':dispatches,
		'dispatch_orders':dispatch_orders}, 
		context)


def get_driver(user):
    for driver in DriverProfile.objects.all():
        if driver.user == user:
            return driver
    return False
