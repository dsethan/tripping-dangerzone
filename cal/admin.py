from django.contrib import admin
from cal.models import Entry

class EntryAdmin(admin.ModelAdmin):
	list_display = ('start_time', 'date', 'deliveries_available', 'restaurant', 'window_length')

admin.site.register(Entry, EntryAdmin)