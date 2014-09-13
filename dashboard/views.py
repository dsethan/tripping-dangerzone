from django.shortcuts import render
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
from orders.models import Order
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

# Create your views here.

def dashboard(request):
	context = RequestContext(request)

	# Get the user profile making the request
	user = request.user

	# Determine whether or not the user is staff w/ access to dashboard
	if user.is_staff:

		# Initialize a list for all of today's orders
		orders = []

		# Initialize an int for total number of orders
		number_orders = 0

		# Initialize an int for total revenues (in cents)
		total_revenues = 0

		# Get all of today's orders
		for order in Order.objects.all():
			if order.entry.date == datetime.date.today()+datetime.timedelta(days=1):
				orders.append(order)

				# Increment total number of orders
				number_orders = number_orders + 1

				# Increment total revenues of orders for today
				total_revenues = total_revenues + order.total


		return render_to_response("dashboard.html",
			{'orders':orders,
			'number_orders':number_orders,
			'total_revenues':total_revenues,},
			context)

	return HttpResponse("No permission")

def order_management(request):
	context = RequestContext(request)

	# Get the user profile of the session
	user = request.user

	# Still need to make sure that the current user is staff
	if user.is_staff:

		# Get today's date
		today = datetime.date.today()# + datetime.timedelta(days=1)

		# Current week will be this week unless it is Friday, Saturday, or Sunday
		current_week = datetime.date.today().isocalendar()[1]
		mon_date = today - datetime.timedelta(days=today.weekday())

		if datetime.date.today().isocalendar()[2] == 5 or datetime.date.today().isocalendar()[2] == 6 or datetime.date.today().isocalendar()[2] == 7:
			current_week = datetime.date.today().isocalendar()[1] + 1
			mon_date = today + datetime.timedelta(days=-today.weekday(), weeks=1)

		# List of all dates
		dates = []

		# Get all dates in with associated orders
		for order in Orders.objects.all():
			dates.append(order.date_in)

		# Place dates after monday into dates
		for i in range(0,7):
			dates.append(mon_date + datetime.timedelta(days=i))


		# Initialize a list of all orders
		orders = []

		# Initialize a directory of lat, lng tuples
		lat_lngs = []

		# Initialize a list of tuples (time, location, distance, estimated delivery time, assigned)
		table_info = []

		print today

		# Place all orders from today into that list
		for order in Order.objects.all():
			if order.entry.date == today:
				orders.append(order)

				address = order.user_profile.address
				city = order.user_profile.city
				state = order.user_profile.state

				addr_string = str(address) + " " + str(city) + " " + str(state)
				sleep(.1)
				api_key = "AIzaSyAUYyU_aUoW5iu_pZZ30U0V_bfdPHQMBQM"
				gmaps = GoogleMaps(api_key)
				geo = gmaps.directions(addr_string, addr_string)
				route = geo['Directions']['Routes'][0]	
				lat, lng = route['Steps'][0]['Point']['coordinates'][1], route['Steps'][0]['Point']['coordinates'][0]
				tupe = (lat, lng)
				lat_lngs.append(tupe)
				restaurant_addr = str(order.restaurant.address1) + " " + str(order.restaurant.city) + " " + str(order.restaurant.state)
				dirs = gmaps.directions(restaurant_addr, addr_string)
				time = dirs['Directions']['Duration']['seconds']
				mins = time/60
				secs = time%60
				time_reformatted = str(mins)+":"+str(secs)

				dist = dirs['Directions']['Distance']['meters']
				in_miles = float(dist*.000621371)
				in_miles_reformatted = str(in_miles)

				driver = "NO DRIVER AT THIS HOUR"

				assigned = False
				for do in DispatchOrder.objects.all():
					if do.order == order:
						assigned = True

				if assigned == False:
					assign_order(order)

				for do in DispatchOrder.objects.all():
					if do.order == order:
						driver = str(do.dispatch.driver.user.first_name)+str(do.dispatch.driver.user.last_name)

				tupe_to_add = (order.entry.start_time, address, in_miles_reformatted, time_reformatted, driver)
				table_info.append(tupe_to_add)

		
		gmap_code = generate_gmap_code(lat_lngs)

		return render_to_response("order_management.html",
			{'today':today, 'lat_lngs':lat_lngs, 'gmap_code':gmap_code, 'table_info':table_info, 'dates':dates},
			context)
	return HttpResponse("No Permission")


def assign_order(order):
	date = order.entry.date
	time = order.entry.start_time

	possible_dispatches = []
	
	if len(Dispatch.objects.all())==0:
		return HttpResponse("NO DISPATCHES LISTED")

	for dispatch in Dispatch.objects.all():
		dispatch_start_min = dispatch.start_time.minute
		dispatch_start_hour = dispatch.start_time.hour
		dummy = datetime.datetime(1, 1, 1, dispatch_start_hour, dispatch_start_min, 00)
		end_time_long = dummy + datetime.timedelta(minutes=dispatch.length)
		end_time = end_time_long.time()
		if (dispatch.date == date) and (dispatch.start_time <= time <= end_time):
			possible_dispatches.append(dispatch)

	dispatch = random.choice(possible_dispatches)

	new_dispatch_order = DispatchOrder(dispatch=dispatch, order=order)

	new_dispatch_order.save()

	print "saved"
	



def create_dispatches(request):
	# Get today's date
	today = datetime.date.today()

	# Current week will be this week unless it is Friday, Saturday, or Sunday
	current_week = datetime.date.today().isocalendar()[1]
	mon_date = today - datetime.timedelta(days=today.weekday())

	if datetime.date.today().isocalendar()[2] == 5 or datetime.date.today().isocalendar()[2] == 6 or datetime.date.today().isocalendar()[2] == 7:
		current_week = datetime.date.today().isocalendar()[1] + 1
		mon_date = today + datetime.timedelta(days=-today.weekday(), weeks=1)

	# Get a list of all days of the week
	days = []

	# And populate it (make 0-5 if weekdays only)
	for i in range(0,7):
		to_add = mon_date + datetime.timedelta(days=i)
		days.append(to_add)

def remove_all_dispatches(request):
	context = RequestContext(request)
	for dispatch in Dispatch.objects.all():
		dispatch.delete()
	return dashboard(request)

def populate_menu(request):
	# Get today's date
	today = datetime.date.today()

	# Current week will be this week unless it is Friday, Saturday, or Sunday
	current_week = datetime.date.today().isocalendar()[1]
	mon_date = today - datetime.timedelta(days=today.weekday())

	if datetime.date.today().isocalendar()[2] == 5 or datetime.date.today().isocalendar()[2] == 6 or datetime.date.today().isocalendar()[2] == 7:
		current_week = datetime.date.today().isocalendar()[1] + 1
		mon_date = today + datetime.timedelta(days=-today.weekday(), weeks=1)

	# Get a list of all days of the week
	days = []

	# And populate it (make 0-5 if weekdays only)
	for i in range(0,7):
		to_add = mon_date + datetime.timedelta(days=i)
		days.append(to_add)

	# Add and save entries

	restaurant = Restaurant.objects.get(id=1)

	for day in days:

		for hour in range(8,10):

			for k in [0, 20, 40]:

				new_entry = Entry(start_time=datetime.time(hour, k),
					date=day,
					deliveries_available=2,
					restaurant=restaurant,
					revenue=0,
					window_length=20)

				new_entry.save()

	print "Successfully populated"

	return dashboard(request)


def depopulate_menu(request):
	# Get today's date
	today = datetime.date.today()

	# Current week will be this week unless it is Friday, Saturday, or Sunday
	current_week = datetime.date.today().isocalendar()[1]
	mon_date = today - datetime.timedelta(days=today.weekday())

	if datetime.date.today().isocalendar()[2] == 5 or datetime.date.today().isocalendar()[2] == 6 or datetime.date.today().isocalendar()[2] == 7:
		current_week = datetime.date.today().isocalendar()[1] + 1
		mon_date = today + datetime.timedelta(days=-today.weekday(), weeks=1)

	# Get a list of all days of the week
	days = []

	# And populate it (make 0-5 if weekdays only)
	for i in range(0,7):
		to_add = mon_date + datetime.timedelta(days=i)
		days.append(to_add)

	# Add and save entries

	for entry in Entry.objects.all():
		if entry.date in days:
			entry.delete()

	print "Successfully depopulated"

	return dashboard(request)

def drivers(request):
	context = RequestContext(request)

	return render_to_response(
		"drivers.html",
		{},
		context)

def assign_times(request):
	context = RequestContext(request)
	user = request.user

	# Get today's date
	today = datetime.date.today()

	# Current week will be this week unless it is Friday, Saturday, or Sunday
	current_week = datetime.date.today().isocalendar()[1]
	mon_date = today - datetime.timedelta(days=today.weekday())

	if datetime.date.today().isocalendar()[2] == 5 or datetime.date.today().isocalendar()[2] == 6 or datetime.date.today().isocalendar()[2] == 7:
		current_week = datetime.date.today().isocalendar()[1] + 1
		mon_date = today + datetime.timedelta(days=-today.weekday(), weeks=1)

	# Get a list of all days of the week
	days = []

	# And populate it (make 0-5 if weekdays only)
	for i in range(0,5):
		to_add = mon_date + datetime.timedelta(days=i)
		days.append(to_add)




	return render_to_response(
		"assign_times.html",
		{'drivers':DriverProfile.objects.all(),
		'days':days,},
		context)

def process_driver_add(request):
	context = RequestContext(request)
	user = request.user

	for item in request.POST:
		if item != "csrfmiddlewaretoken":
			spl = item.split(":")
			date = spl[0]
			driver_id = spl[1]

			for k in create_times(8,00,10,00,20):

				new_dispatch = Dispatch(date=date, 
					start_time=k,
					length=20,
					driver=DriverProfile.objects.get(id=driver_id))
				new_dispatch.save()

	return dashboard(request)


def create_times(start_time_hr, start_time_min, end_time_hr, end_time_min, window_length):
	times = []

	start_time = datetime.datetime(1, 1, 1, start_time_hr, start_time_min, 00)
	end_time = datetime.datetime(1, 1, 1, end_time_hr, end_time_min, 00)


	while start_time + datetime.timedelta(minutes=window_length) < end_time:
		times.append(start_time.time())
		start_time = start_time + timedelta(minutes=window_length)

	return times

def add_driver(request):
	context = RequestContext(request)
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
	restaurants = Restaurant.objects.all()

	if request.method == 'POST':
		username = request.POST.get('username')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		restaurant_id = request.POST.get('restaurant')
		restaurant = Restaurant.objects.get(id=restaurant_id)

		if password == password2:
			new_user = User(username=username,
				first_name=first_name,
				last_name=last_name)
			new_user.set_password(password)
			new_user.save()

			driver = DriverProfile(
				user=new_user,
				city="Durham",
				state="NC",
				restaurant=restaurant,
				)
			driver.save()

			print "Successfully added driver"

			return render_to_response(
				"confirm_driver_add.html",
				{},
				context)
		else:
			error = "Passwords do not match"
			return render_to_response(
				"add_driver.html",
				{'restaurants':restaurants, 
				'error':error },
				context)

	return render_to_response(
		"add_driver.html",
		{'restaurants':restaurants},
		context)

def data(request):
	context = RequestContext(request)
	return HttpResponse("data")

def financials(request):
	context = RequestContext(request)
	return HttpResponse("financials")

def generate_gmap_code(lat_lngs):
	start_string = """
		<html>
		  <head>
		    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
		    <meta charset="utf-8">
		    <title>Order Management</title>
		    <style>
		      html, body, #map-canvas {
		        height: 100%;
		        margin: 0px;
		        padding: 0px
		      }
		    </style>
		    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
		    <script>
		function initialize() {
		  var myLatlng = new google.maps.LatLng(35.996597,-78.915869);
		  var mapOptions = {
		    zoom: 14,
		    center: myLatlng
		  }
		  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

		var myLatLng = new google.maps.LatLng(35.996597,-78.915869);

				var marker = new google.maps.Marker({position: myLatLng,
					map: map, 
					title:'Hello'});


		"""
	for lat_lng in lat_lngs:
		start_string = start_string + """

		var myLatLng = new google.maps.LatLng("""+str(lat_lng[0])+""","""+str(lat_lng[1])+""");

		var marker = new google.maps.Marker({position: myLatLng,
			map: map, 
			title:'Hello'});"""


	start_string = start_string + """} 
	google.maps.event.addDomListener(window, 'load', initialize); 
	</script>"""

	return start_string

