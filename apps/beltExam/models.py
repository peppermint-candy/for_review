from __future__ import unicode_literals
from django.db import models
# from .models import User
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')
NAME = re.compile(r'[0,1,2,3,4,5,6,7,8,9]')

# Create your models here.
class UserManager(models.Manager):
	def login(self, email, password):
		activeU = self.filter(email__iexact = email)
		if activeU and bcrypt.hashpw(password.encode("utf-8") , activeU[0].password.encode("utf-8")) == activeU[0].password:
			#should be classified as a succesful login
			return (True, activeU[0])
		else:
			return(False, {"login" : "login failed, please try again"})

	def register(self,first_name, alias, email, password, confirm_password):
		errors = {}

		if len(first_name) <2 :
			errors['first_name'] = "First Name is too short"
		if NAME.match(first_name):
			errors['name1'] = "First name cannot contain number(s)"
		if len(alias) <2 :
			errors['alias'] = "Alias is too short"
		if len(password) < 8 :
			errors['password'] = "Password is too short"
		if password != confirm_password:
			errors['confirm_password'] = "Password must match"
		if not EMAIL_REGEX.match(email):
			errors['email'] = "Please enter a valid email"
		user = self.filter(email__iexact = email)

		try:
			user[0]
			errors['invalid'] = "Invalid registration"
		except:
			pass

		if errors:
			return (False, errors)
		else:
		#register this person!
			hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
			self.create(first_name = first_name, alias = alias, email = email, password = hash_password)
			return (True, self.filter(email = email)[0])

class User(models.Model):
	first_name = models.CharField(max_length=45)
	alias = models.CharField(max_length=45)
	email = models.EmailField()
	password = models.CharField(max_length=255)
	# dob = models.DateField(auto_now=False, auto_now_add=False)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	userManager = UserManager()
	objects = models.Manager()


class Poke(models.Model):
	userpoke = models.ForeignKey(User, related_name = "p1")
	userpoked = models.ForeignKey(User, related_name ="p2")
	poked = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now=True)