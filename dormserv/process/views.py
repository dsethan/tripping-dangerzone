from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from cal.models import Entry
from item.models import Item
from users.models import User, UserProfile
from orders.models import Order
from pkg.models import Cart, CartItem
from orders.models import Order, OrderItem
from checkout.views import checkout

def process_order(request):
	context = RequestContext(request)
	user = request.user
	profile = get_associated_profile(user)
	cart = get_cart(profile)

	items_to_package = []
	total_price = 0
	for item in CartItem.objects.all():
		if item.cart == cart:
			items_to_package.append(item.item)
			total_price = total_price + item.item.price

	entry_id = request.POST.get('entry_id')
	entry = Entry.objects.get(id=entry_id)

	new_order = Order(user_profile=profile, 
		restaurant=profile.restaurant, 
		total = total_price,
		entry = entry,
		status = 'PDG',
		order_success = False,
		order_rating = 0
		)

	new_order.save()

	order_dict = {}

	for item in items_to_package:
		if item.id in order_dict.keys():
			order_dict[item.id] = order_dict[item.id] + 1
		else:
			order_dict[item.id] = 1

	for key in order_dict.keys():
		item = Item.objects.get(id=key)
		quantity = order_dict[key]
		new_order_item = OrderItem(item=item,
			order=new_order,
			quantity=quantity)
		new_order_item.save()

	cart.delete()
	return redirect('checkout.views.checkout')

def get_cart(user_profile):
	for cart in Cart.objects.all():
		if cart.profile == user_profile:
			return cart
	return False

def get_associated_profile(user):
	for up in UserProfile.objects.all():
		if up.user.id == user.id:
			return up
	return None

def increment_clicks(user):
	profile = get_associated_profile(user)
	profile.clicks = profile.clicks + 1
	profile.save()