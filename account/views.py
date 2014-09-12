from django.shortcuts import render_to_response
from cal.models import Entry
from users.models import User, UserProfile
from django.template import RequestContext

def display_account(request):
	context = RequestContext(request)
	user = request.user
	increment_clicks(user)
	return render_to_response(
		'account.html',
		{'user':user,},
		context)

def get_associated_profile(user):
	for up in UserProfile.objects.all():
		if up.user.id == user.id:
			return up
	return None

def increment_clicks(user):
	profile = get_associated_profile(user)
	profile.clicks = profile.clicks + 1
	profile.save()
