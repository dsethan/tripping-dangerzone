from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from cal.models import Entry
from item.models import Item
from users.models import User, UserProfile
from orders.models import Order
from pkg.models import Cart, CartItem

# need to make sure to destroy cart object.


def display_menu(request):
	context = RequestContext(request)
	user = request.user
	increment_clicks(user)
	profile = get_associated_profile(user)
	if request.method == 'POST':
		entry_id = request.POST.get('entry_id')
		entry = Entry.objects.get(id=entry_id)

		if not cart_exists(profile):
			new_cart = Cart(profile=profile, total=0)
			new_cart.save()
		else:
			get_cart(profile)



		items = []
		for item in Item.objects.all():
			items.append(item)

		return render_to_response(
			'menu.html',
			{'entry':entry, 'entry_id':entry_id, 'user':user, 'profile':profile, 'items':items},
			context)
	#Else statement for if not post
	return HttpResponse("Menu!")




def add_item(request):
	context = RequestContext(request)
	user = request.user
	increment_clicks(user)
	profile = get_associated_profile(user)

	if request.method == 'POST':
		item_id = request.POST.get('item.id')
		item = Item.objects.get(id=item_id)
		print item
		cart = get_cart(profile)
		cart_item = CartItem(cart=cart, item=item, qty=1)
		cart_item.save()

		# for test only
		print cart.id
		for cart_item in CartItem.objects.all():
			if cart_item.cart.id == cart.id:
				print cart_item.item
		print "\n"

	return display_menu(request)

def get_cart(user_profile):
	for cart in Cart.objects.all():
		if cart.profile == user_profile:
			return cart
	return False

def cart_exists(user_profile):

	for cart in Cart.objects.all():
		if cart.profile == user_profile:
			return True
	return False


def order_exists(entry_id, profile):
	indicator = False
	for order in Order.objects.all():
		if (order.entry.id == entry_id) and (order.user_profile.id == profile.id):
			indicator = True
	return indicator

def get_order(entry_id, profile):
	for order in Order.objects.all():
		if (order.entry.id == entry_id) and (order.user_profile.id == profile.id):
			return order
	return HttpResponse("Error")

def get_associated_profile(user):
	for up in UserProfile.objects.all():
		if up.user.id == user.id:
			return up
	return None

def increment_clicks(user):
	profile = get_associated_profile(user)
	profile.clicks = profile.clicks + 1
	profile.save()
