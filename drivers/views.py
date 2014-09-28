from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from dispatch.models import Dispatch, DispatchOrder
from drivers.models import DriverProfile
from users.models import User, UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date, time
# Create your views here.

def driver_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    cur_usr = request.user

    if cur_usr.is_active:
        if is_driver(cur_usr):
            return redirect('driver_dash')

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.

                if is_driver(user):
                    login(request, user)
                    return redirect('driver_dash')
                else:
                    return HttpResponse("Sorry, you are not a driver.")
            else:
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            #print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response('login_error.html', {}, context)
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('driver_login.html', {}, context)


def order_update(request):
    context = RequestContext(request)

    # Make sure it is a HTTP POST request
    if request.method == 'POST':

        # Get the id of the order submitted
        order_id = int(request.POST.get('order_id'))

        # Change delivered field
        order_to_update = Order.objects.get(id=order_id)
        order_to_update.order_success = True

        return driver_dash(request)

    return driver_dash(request)


def is_driver(user):
    for driver in DriverProfile.objects.all():
        if driver.user == user:
            return True
    return False

def driver_dash(request):
	context = RequestContext(request)

	# Get associated DriverProfile for the current user.
	user = request.user
	driver = get_driver(user)

	# Initialize a list of all dispatches for the current driver
	dispatches = []

    # Get today's date
    today = datetime.date.today()

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
		'dispatch_orders':dispatch_orders,
        'today':today}, 
		context)


def get_driver(user):
    for driver in DriverProfile.objects.all():
        if driver.user == user:
            return driver
    return False
