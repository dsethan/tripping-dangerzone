from cal.models import Entry
from item.models import Item
import datetime
from django.utils import timezone
from datetime import date, time, timedelta
from restaurants.models import Restaurant

def populate_week():
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

	restaurant = restaurant.objects.get(id=0)

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


if __name__ == "__main__":
	populate_week()
