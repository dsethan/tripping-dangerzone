from django.shortcuts import render
from dispatch.models import Dispatch, DispatchOrder
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
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


def kitchen(request):
	context = RequestContext(request)
	user = request.user

	if user.is_staff:
		today = datetime.date.today() - datetime.timedelta(days=1)
		dispatches = {}


		for order in DispatchOrder.objects.all():
			if order.dispatch.date == today:
				dispatch = order.dispatch
				
				if dispatch not in dispatches.keys():
					dispatches[dispatch] = []

				current_list = dispatches[dispatch]

				current_list.append(order)


		return render_to_response(
			'kitchen.html',
			{'dispatches':dispatches},
			context)


	return HttpResponse("No permission")


# Create your views here.
