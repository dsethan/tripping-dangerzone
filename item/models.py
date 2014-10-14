from django.db import models

class Item(models.Model):
	HOT = 'HOT'
	COLD = 'COLD'
	PRE = 'PRE'
	PREP_CATEGORIES = (
		(HOT, 'HOT'),
		(COLD, 'COLD'),
		(PRE, 'PRE'),
		)
	name = models.CharField(max_length=50)
	price = models.IntegerField(default=0) # in cents
	cost = models.IntegerField(default=0) # in cents
	description = models.TextField(max_length=10)
	prep_category = models.CharField(max_length=5,choices=PREP_CATEGORIES)
	number_ordered = models.IntegerField(default=0)
	total_spent = models.IntegerField(default=0)
	available = models.BooleanField(default=False)

	def format_price_usd(self):
		if len(self.price) == 2:
			return "$" + "0." + str(self.price)
		if len(self.price) > 2:
			print "hi"
			price_string = str(self.price)
			print "$" + price_string[0:len(price_string)-2] + "." + price_string[len(price_string)-2:len(price_string)]
			return "$" + price_string[0:len(price_string)-2] + "." + price_string[len(price_string)-2:len(price_string)]

	def view_order_total_in_usd(self):
		self_str = str(self.price)
		cents = self_str[-2:]
		dollars = self_str[:-2]
		return "$" + dollars + "." + cents

		return "issue"
	def __unicode__(self):
		return self.name