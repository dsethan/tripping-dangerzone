from django import forms
import re
from users.models import UserProfile
from django.contrib.auth.models import User
from googlemaps import GoogleMaps

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())

	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", username):
			raise forms.ValidationError('Please enter a valid email address.')
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('A user with that email has already registered.')

	def clean_password(self):
		password = self.cleaned_data['password']
		if len(password) < 5:
			raise forms.ValidationError('Passwords must be at least 5 characters long.')
		return password

	def clean(self):
	    """                                                                                                                                                                                                                                                  
	    Verifiy that the values entered into the two password fields                                                                                                                                                                                         
	    match. Note that an error here will end up in                                                                                                                                                                                                        
	    ``non_field_errors()`` because it doesn't apply to a single                                                                                                                                                                                          
	    field.                                                                                                                                                                                                                                               

	    """
	    if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
	        if self.cleaned_data['password'] != self.cleaned_data['password2']:
	        	raise forms.ValidationError('Your passwords do not match.')

	    return self.cleaned_data


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password', 'password2')


class UserProfileForm(forms.ModelForm):

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		raw_phone_str = ""
		for i in range(len(phone)):
			if phone[i] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
				raw_phone_str = raw_phone_str + phone[i]
    
		if len(raw_phone_str) < 10:
			raise forms.ValidationError('Please enter a valid phone number.')

		if len(raw_phone_str) == 10:
			raw_phone_str = "1" + raw_phone_str

		clean_phone = "+" + raw_phone_str
		return clean_phone


	class Meta:
		model = UserProfile
		fields = ('address', 'city', 'state', 'phone', )