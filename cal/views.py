from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from cal.models import Entry
from users.models import UserProfile, User
from django.utils import timezone
import datetime
from datetime import date, time, timedelta
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from twilio.rest import TwilioRestClient
from random import randint
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

@login_required
def display_calendar(request):
	# Get all pertinent user information and increase num of clicks
	context = RequestContext(request)
	user = request.user
	profile = get_associated_profile(user)
	profile.clicks = profile.clicks + 1
	profile.save()
	restaurant = profile.restaurant
	today = datetime.date.today()

	# Current week will be this week unless it is Friday, Saturday, or Sunday
	current_week = datetime.date.today().isocalendar()[1]
	mon_date = today - datetime.timedelta(days=today.weekday())

	if datetime.date.today().isocalendar()[2] == 5 or datetime.date.today().isocalendar()[2] == 6 or datetime.date.today().isocalendar()[2] == 7:
		current_week = datetime.date.today().isocalendar()[1] + 1
		mon_date = today + datetime.timedelta(days=-today.weekday(), weeks=1)

	# Get all entries that are this week into a directory FROM THE RESTAURANT
	weekly_entries = []

	for entry in Entry.objects.all():
		if entry.restaurant == restaurant:
			if entry.week_num() == current_week:
				weekly_entries.append(entry)

	mon, tues, wed, thurs, fri, sat, sun = [], [], [], [], [], [], []

	for entry in weekly_entries:
		if entry.week_day() == 1:
			mon.append(entry)
			mon_date = entry.date
		if entry.week_day() == 2:
			tues.append(entry)
		if entry.week_day() == 3:
			wed.append(entry)
		if entry.week_day() == 4:
			thurs.append(entry)
		if entry.week_day() == 5:
			fri.append(entry)
		if entry.week_day() == 6:
			sat.append(entry)
		if entry.week_day() == 7:
			sun.append(entry)

	dates = []
	for i in range(0,7):
		date_to_add = mon_date + timedelta(days=i)
		dates.append(date_to_add.strftime("%m/%d"))

	mon = sort_time(mon)
	tues = sort_time(tues)
	wed = sort_time(wed)
	thurs = sort_time(thurs)
	fri = sort_time(fri)
	sat = sort_time(sat)
	sun = sort_time(sun)

	return render_to_response(
		'cal.html',
		{'mon':mon, 'tues':tues, 'wed':wed, 'thurs':thurs, 'fri':fri, 'sat':sat, 'sun':sun, 'dates':dates, 'user':user, 'profile':profile},
		context)

def increment_clicks(user):
	profile = get_associated_profile(user)
	profile.clicks = profile.clicks + 1
	profile.save()

@login_required
def menu_reroute(request):
	context = RequestContext(request)

def sort_time(time_list):
	sorted_times = []
	for time in time_list:
		cur = time.start_time.strftime("%I:%M")
		sorted_times.append(cur)
	sorted_times = sorted(sorted_times)
	elem_list = []
	for k in sorted_times:
		for time in time_list:
			if k == time.start_time.strftime("%I:%M"):
				elem_list.append(time)
	return elem_list

def get_associated_profile(user):
	for up in UserProfile.objects.all():
		if up.user.id == user.id:
			return up
	return None