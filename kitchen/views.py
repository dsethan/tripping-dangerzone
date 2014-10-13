from django.shortcuts import render
from dispatch.models import Dispatch, DispatchOrder
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
import django.contrib.auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from dispatch.models import Dispatch, DispatchOrder
import datetime
from datetime import date, time, timedelta
from orders.models import Order, OrderItem
from cal.models import Entry
from item.models import Item
from django.utils import timezone
from restaurants.models import Restaurant
from googlemaps import GoogleMaps
from users.models import User, UserProfile
from drivers.models import DriverProfile
from users.forms import UserForm
from time import sleep
import random


def kitchen_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    cur_usr = request.user

    if cur_usr.is_active:
        if cur_usr.is_staff:
            return redirect('kitchen_dash')

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

                if user.is_staff:
                    login(request, user)
                    return redirect('kitchen_dash')
                else:
                    return HttpResponse("Sorry, staff only.")
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
        return render_to_response('kitchen_login.html', {}, context)


def kitchen_dash(request):
	context = RequestContext(request)
	user = request.user

	if user.is_staff:
		today = datetime.date.today() #- datetime.timedelta(days=1)
		dispatches = {}


		for order in DispatchOrder.objects.all():
			if order.dispatch.date == today:
				dispatch = order.dispatch
				
				if dispatch not in dispatches.keys():
					dispatches[dispatch] = []

				current_list = dispatches[dispatch]

				current_list.append(order)

		orderitem = []

		for item in OrderItem.objects.all():
			if item.order.entry.date == today:
				orderitem.append(item)

		return render_to_response(
			'kitchen.html',
			{'dispatches':dispatches,
			'orderitem':orderitem},
			context)
		h
	return HttpResponse("No permission")


# Create your views here.
