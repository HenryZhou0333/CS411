from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
# Create your models here.

class Courses(models.Model):
	id = models.CharField(max_length = 50, primary_key=True)
	name = models.CharField(max_length = 100, blank = True)
	description = models.TextField(blank = True)
	language = models.CharField(max_length = 50, blank = True)
	photo = models.CharField(max_length = 300, blank = True)
	workload = models.CharField(max_length = 100, blank = True)
	previewLink = models.CharField(max_length = 300, blank = True)

	def __str__(self):
		return self.name

class Categories(models.Model):
	category_name = models.CharField(max_length = 100)
	course_id = models.CharField(max_length = 50)


class Instructors(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length = 100, blank = True)
	bio = models.TextField(blank = True)
	photo = models.CharField(max_length = 300, blank = True)
	title = models.CharField(max_length = 100, blank = True)
	website = models.CharField(max_length = 300, blank = True)
	department = models.CharField(max_length = 100, blank = True)

	def __str__(self):
		return self.name


class Institutions(models.Model):
	id = models.CharField(max_length = 50, primary_key=True)
	name = models.CharField(max_length = 100, blank = True)
	description = models.TextField(blank = True)
	links = JSONField(blank = True)
	location = JSONField(blank = True)

	def __str__(self):
		return self.name


class Users(models.Model):
	username = models.CharField(max_length = 50, primary_key=True)
	email = models.EmailField()
	password = models.CharField(max_length = 50)

	def __str__(self):
		return self.username


class Like(models.Model):
	username = models.CharField(max_length = 50)
	course_id = models.CharField(max_length = 50)


class Teach(models.Model):
	instructors_id = models.IntegerField()
	course_id = models.CharField(max_length = 50)


class Offer(models.Model):
	institution_id =  models.CharField(max_length = 50)
	course_id = models.CharField(max_length = 50)

