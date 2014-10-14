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
from checkout.models import CustomerProfile
import stripe
# Create your views here.


def process_order(request):
	context = RequestContext(request)
	user = request.user
	increment_clicks(user)
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

	total_price = new_order.view_order_total_in_usd()

	order_dict = {}

	for item in items_to_package:
		if item.id in order_dict.keys():
			order_dict[item.id] = order_dict[item.id] + 1
		else:
			order_dict[item.id] = 1


	order_items = []
	for key in order_dict.keys():
		item = Item.objects.get(id=key)
		quantity = order_dict[key]
		new_order_item = OrderItem(item=item,
			order=new_order,
			quantity=quantity)
		new_order_item.save()
		order_items.append(new_order_item)

	#cart.delete()

	#print order_dict.keys()
	cart_id = cart.id
	print cart.id


	return render_to_response("confirm.html", {'total_price':total_price, 'user':user, 'profile':profile, 'order_items':order_items, 'cart_id':cart_id }, context)


def process(request):
	context = RequestContext(request)
	user = request.user
	profile = get_associated_profile(user)
	increment_clicks(user)

	# Set your secret key: remember to change this to your live secret key in production
	# See your keys here https://dashboard.stripe.com/account
	stripe.api_key = "sk_test_gii6sAzH4fvDd6xCENhAgb9j"

	if request.method == 'POST':
		cart_id = request.POST.get('cart_id')
		print cart_id
		Cart.objects.get(id=cart_id).delete()

		total_price = request.POST.get('total_price')

		# Get the credit card details submitted by the form
		token = request.POST['stripeToken']

		if not get_associated_customer(profile) == False:
			customer = get_associated_customer(profile)
			customer_id = customer.customer_id

			stripe.Charge.create(
				amount=int(total_price),
				currency="usd",
				customer=customer_id
			)

		else:
			customer = stripe.Customer.create(
				card = token,
				description = profile.user.email
			)

			stripe.Charge.create(
			    amount=int(total_price), # incents 
			    currency="usd",
			    customer=customer.id
			)

			new_customer_profile = CustomerProfile(profile=profile, customer_id=customer.id)
			new_customer_profile.save()

		return render_to_response(
			'successful_charge.html',
			{},
			context)


	return HttpResponse("Something went wrong")

def get_associated_customer(profile):
	for cust in CustomerProfile.objects.all():
		if cust.profile == profile:
			return cust
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

def get_cart(user_profile):
	for cart in Cart.objects.all():
		if cart.profile == user_profile:
			return cart
	return False
