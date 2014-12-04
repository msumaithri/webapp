from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# to store the non-trivial information about a user
class User_information (models.Model):
	user = models.ForeignKey(User)
	phone_number = models.CharField(blank=True, null=True, max_length=16)
	dob = models.DateField()
	door_number = models.CharField(blank=True, null=True, max_length=12)
	street = models.CharField(max_length=20)
	city = models.CharField(max_length=30)
	pincode = models.CharField(max_length=10)
	state=models.CharField(max_length=20)
	country = models.CharField(max_length=30)
	picture = models.ImageField("Profile Picture", upload_to="profile-pic", blank=True)

class Rating (models.Model):
	user = models.ForeignKey(User)
	rating_stars = models.IntegerField(default=0)
	rating_cumulative = models.IntegerField(default=0)
	rating_count = models.IntegerField(default=0)

# testimonial for a user's service
class Testimonial (models.Model):
	user_whoGave = models.CharField(max_length=20)
	user_whoReceived = models.CharField(max_length=20)
	content = models.TextField(max_length=150)
	testimonial_date = models.DateTimeField(default=datetime.now, blank=True)
	rating_display = models.CharField(max_length=5, blank=True)
	rating = models.IntegerField(default=0)

class Discussion (models.Model):
	participant1 = models.CharField(max_length=15)
	participant2 = models.CharField(max_length=15)
	task_id = models.IntegerField(default=0)

# the chat that is private to two users 
class Comments (models.Model):
	comment_info = models.CharField(max_length=100)
	discussion_id = models.IntegerField(default=0)
	comment_date = models.DateTimeField()
	task_id = models.IntegerField(default=0)
	comment_owner = models.CharField(max_length=15)

# to maintain the list of users who have accepted a particular taks
class TaskQueue (models.Model):
	task = models.IntegerField(default=0)
	discussion_id = models.IntegerField(default=0)
	user = models.ForeignKey(User)

# to do some household chores
class Service (models.Model):
	door_number = models.CharField(blank=True, null=True, max_length=12)
	street = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	pincode = models.CharField(max_length=10)
	state=models.CharField(max_length=20)
	country = models.CharField(max_length=30)
	user_delivering = models.ForeignKey(User_information,blank=True, null=True)
	user_ordering = models.ForeignKey(User)
	deadline = models.DateField()
	money_paid = models.IntegerField(default=1)
	task_details = models.TextField(max_length=200)
	task_name=models.CharField(max_length=100)
	task_type=models.CharField(max_length=20)
	task_post_date = models.DateTimeField(default=datetime.now, blank=True)
	task_status = models.CharField(default="open", max_length=10)
