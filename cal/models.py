from django.db import models
from item.models import Item
import datetime
from django.utils import timezone
from datetime import date, time, timedelta
from restaurants.models import Restaurant

class Entry(models.Model):
	start_time = models.TimeField()
	date = models.DateField(auto_now=False)
	deliveries_available = models.IntegerField(default=2)
	restaurant = models.ForeignKey(Restaurant)
	revenue = models.IntegerField(default = 0)
	window_length = models.IntegerField(default=20)

	def week_num(self):
		iso = self.date.isocalendar()
		return iso[1]

	def week_day(self):
		iso = self.date.isocalendar()
		return iso[2]

	def end_time(self):
		date_string - self.date.strftiem("%Y:%m:%d").split(":")
		time_string = self.start_time.strftime("%I:%M").split(":")
		reformatted_date = datetime.datetime(int(date_string[0]), int(date_string[1]), int(date_string[2]), int(time_string[0]), int(time_string[1]), 00)
		return reformatted_date + datetime.timedelta(minutes=self.window_length)

	def display_entry(self):
		date_info = self.date.strftime("%Y:%m:%d")
		time_info = self.start_time.strftime("%I:%M")
		return "Entry " + self.id + " " + date_info + " " + time_info

	def display_time(self):
		t = self.start_time.strftime("%I:%M")
		if t[0] == "0":
			return t[1:] + " am"
		return t + " am"

	def twenty_over(self):
		d_ref = self.date.strftime("%Y:%m:%d")
		d_ref_spl = d_ref.split(":")
		t_ref = self.start_time.strftime("%I:%M")
		t_ref_spl = t_ref.split(":")
		dt = datetime.datetime(int(d_ref_spl[0]), int(d_ref_spl[1]), int(d_ref_spl[2]), int(t_ref_spl[0]), int(t_ref_spl[1]), 00)
		time_of_concern = dt + datetime.timedelta(minutes=self.window_length)
		t = time_of_concern.strftime("%I:%M")
		if t[0] == "0":
			return t[1:] + " am"
		return t + " am"

	def entry_open(self):
		if deliveries_available > 0:
			return True
		return False


	def is_active(self):
		#if self.date.strftime("%Y:%m:%d") == datetime.now().strftime("%Y:%m:%d"):
		#	if int(datetime.now().strftime("%H")) >= 7:
		#		return False
		if (datetime.datetime.now().isocalendar()[1] == self.date.isocalendar()[1]) and (datetime.datetime.now().isocalendar()[2] == self.date.isocalendar()[2]) and int(self.start_time.strftime("%H")) > 6:
			return False

		if self.deliveries_available > 0:
			return True

		return False

	def __unicode__(self):
		return "Id: " + str(self.id) + " | " + self.date.strftime("%m/%d/%Y") + " " + self.start_time.strftime("%I:%M")

