from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from users.models import User, UserProfile
from users.forms import UserForm, UserProfileForm
from drivers.models import DriverProfile
from restaurants.models import Restaurant
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from users.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from random import randint
from twilio.rest import TwilioRestClient
from googlemaps import GoogleMaps

def update_view_data(request):
    context = RequestContext(request)
    current_user = request.user

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
        
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            restaurant_boolean = find_restaurant(context, profile.address, profile.city, profile.state)

            if restaurant_boolean[0] == True:
            	profile.restaurant = restaurant_boolean[1]

            else:
            	return HttpResponse("Unfortunately, we are not currently serving your area. Please try again soon.")

            profile.user = user
            print profile.address


            # Now we save the UserProfile model instance.
            profile.save()
            r0 = randint(0, 9)
            r1 = randint(0, 9)
            r2 = randint(0, 9)
            r3 = randint(0, 9)
            str_sec = str(r0)+str(r1)+str(r2)+str(r3)

            account_sid = "ACd2d6a002416aad11df6d7b3d529506b2"
            auth_token = "616085bee1e2c14db70339a86bfa9dda"
            client = TwilioRestClient(account_sid, auth_token)
            message = client.sms.messages.create(body=user.first_name + ", thanks for signing up for Dormserv! Your code is " + str_sec, to= profile.phone, from_="+19146185355") # Replace with your Twilio number
            registered = True
            return render_to_response('confirm_account.html',
                {'profile': profile.id, 'user':profile.user.id, 'str_sec':str_sec},
                context)

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def find_restaurant(request, address, city, state):
	start = address + " " + city + " " + state
	for restaurant in Restaurant.objects.all():
		api_key = "AIzaSyAUYyU_aUoW5iu_pZZ30U0V_bfdPHQMBQM"
		gmaps = GoogleMaps(api_key)
		end = restaurant.get_address()
		dirs = gmaps.directions(start, end)
		dist = dirs['Directions']['Distance']['meters']
		print "Dist: " + str(dist)
		if dist < restaurant.max_radius:
			print restaurant
			return (True, restaurant)
		else:
			#print "getting false"
			return (False, "")

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    cur_usr = request.user

    if cur_usr.is_active:
        if is_driver(cur_usr):
            return redirect('/drivers', user=cur_usr)
        return redirect('/cal', user=cur_usr)

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

                login(request, user)

                if is_driver(user):
                    return redirect('/drivers', user=user)
               	# cur_user_profile = UserProfile.get(id=user.id)

                profile = get_associated_profile(user)
                profile.logins = profile.logins + 1
                profile.clicks = profile.clicks + 1
                profile.save()

                return redirect('/cal', user=user)

                #return render_to_response('welcome.html', {'user' : user}, context)
            else:
                # An inactive account was used - no logging in!
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
        return render_to_response('login.html', {}, context)


def is_driver(user):
    for driver in DriverProfile.objects.all():
        if driver.user == user:
            return True
    return False



def verify_user_text(request):
    context = RequestContext(request)
    if request.method == 'POST':
        str_sec=request.POST.get('str_sec')
        secret_code=request.POST.get('secret_code')
        profile=request.POST.get('profile')
        user=request.POST.get('user')
        if secret_code == str_sec:
            return render_to_response('login_form.html', {}, context)
        else:
            UserProfile.objects.get(id=profile).delete()
            User.objects.get(id=user).delete()
            return render_to_response("register_2.html", {}, context)
    return HttpResponse("error....")

def get_associated_profile(user):
	for up in UserProfile.objects.all():
		if up.user.id == user.id:
			return up
	return None

def thanks(request):
	return HttpResponse("Thank you for registering!")
	
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    context = RequestContext(request)
    user = request.user

    if is_driver(user):

        logout(request)
        return HttpResponseRedirect('/')

    profile = get_associated_profile(user)
    profile.clicks = profile.clicks + 1
    profile.save()

    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def faq(request):
    context = RequestContext(request)
    form = "Hello"
    return render_to_response('faq.html', {'form': form}, context)

def contact(request):
    context = RequestContext(request)
    form = "Hello"
    return render_to_response('contact.html', {'form': form}, context)

def privacy(request):
    context = RequestContext(request)
    form = "Hello"
    return render_to_response('privacy.html', {'form': form}, context)


