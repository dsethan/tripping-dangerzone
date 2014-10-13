from cal.models import Entry
from item.models import Item
import datetime
from django.utils import timezone
from datetime import date, time, timedelta
from restaurants.models import Restaurant

def populate_week():


	dates = [13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 27, 28]
	days = []
	for date in dates:
		d = datetime.date(2014, 10, date)
		days.append(d)

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
