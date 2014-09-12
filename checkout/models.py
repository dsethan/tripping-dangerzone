from django.db import models
from users.models import User, UserProfile

class CustomerProfile(models.Model):
	profile = models.ForeignKey(UserProfile)
	customer_id = models.CharField(max_length=18)
# Create your models here.
