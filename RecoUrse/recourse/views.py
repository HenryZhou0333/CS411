from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from .models import Courses,Instructors,Institutions,Users,Like,Teach,Offer,Similar
from django.db import connection
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
import datetime

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Create your views here.
@login_required
def index(request):
	# how to retrieve current user's data
	#context = {
	#'username': request.user.username,
	#}
	return render(request, 'recourse/index.html')

# courses
@login_required
def course_search(request):
	list = request.GET.get('courseName')
	list = '%' + list + '%'
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM recourse_courses WHERE name LIKE %s;", list)
	courses_list = dictfetchall(cursor)
	context = {
	'courses_list': courses_list,
	}
	return render(request, 'recourse/course_list.html', context)

@login_required
def course_detail(request, course_id):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM recourse_courses WHERE id = %s;", course_id)
	course = dictfetchall(cursor)
	if len(course)>0:
		course = course[0]
	else:
		raise Http404("Invalid course id.")
	cursor.execute("SELECT * FROM recourse_like WHERE username = %s AND course_id = %s;", (request.user.username,course_id))
	likes = dictfetchall(cursor)
	like = True
	if len(likes)>0:
		like = True
	else:
		like = False

	cursor.execute("SELECT * FROM recourse_courses WHERE id IN (SELECT course2_id FROM recourse_similar WHERE course1_id = %s);",course_id)
	similar = dictfetchall(cursor)

	cursor.execute("SELECT YEAR(time) AS year, MONTH(time) AS month, COUNT(*) AS count from recourse_like where course_id=%s GROUP BY YEAR(time), MONTH(time);", course_id)
	data_pts = dictfetchall(cursor)
	data_= [{'year':2014,'month':1, 'count':0},{'year':2014,'month':2, 'count':0},{'year':2014,'month':3, 'count':0},{'year':2014,'month':4, 'count':0},
			{'year':2014,'month':5, 'count':0},{'year':2014,'month':6, 'count':0},{'year':2014,'month':7, 'count':0},{'year':2014,'month':8, 'count':0},
			{'year':2014,'month':9, 'count':0},{'year':2014,'month':10, 'count':0},{'year':2014,'month':11, 'count':0},{'year':2014,'month':12, 'count':0},
			{'year':2015,'month':1, 'count':0},{'year':2015,'month':2, 'count':0},{'year':2015,'month':3, 'count':0},{'year':2015,'month':4, 'count':0},
			{'year':2015,'month':5, 'count':0},{'year':2015,'month':6, 'count':0},{'year':2015,'month':7, 'count':0},{'year':2015,'month':8, 'count':0},
			{'year':2015,'month':9, 'count':0},{'year':2015,'month':10, 'count':0},{'year':2015,'month':11, 'count':0},{'year':2015,'month':12, 'count':0},
			{'year':2016,'month':1, 'count':0},{'year':2016,'month':2, 'count':0},{'year':2016,'month':3, 'count':0},{'year':2016,'month':4, 'count':0},
			]
	for i in range(0,len(data_pts)):
		index = 12 * (data_pts[i]['year'] - 2014) + data_pts[i]['month']
		data_[index - 1]['count'] += data_pts[i]['count']

	cursor.execute("SELECT count(*) AS count, category_name FROM recourse_categories a, (SELECT course_id FROM recourse_like c1, (SELECT username, time FROM recourse_like WHERE course_id = %s) c3  WHERE c1.username = c3.username AND c1.time > c3.time) b WHERE a.course_id = b.course_id GROUP BY category_name;",course_id)
	courseTookAfter = dictfetchall(cursor)

	context = {
	'course': course,
	'like' : like,
	'similar': similar,
	'data': json.dumps(data_),
	'courseTookAfter': json.dumps(courseTookAfter),
	}

	return render(request, 'recourse/course_details.html', context)


# instructor
@login_required
def instructor_list(request):
	pageNum = 1
	if 'instrPage' in request.GET:
		pageNum = (int)(request.GET.get('instrPage'))
	offset = (pageNum-1) * 100
	cursor = connection.cursor()
	cursor.execute("SELECT id, name FROM recourse_instructors ORDER BY id ASC LIMIT 100 OFFSET %s;", offset)
	instructor_list = dictfetchall(cursor)
	list_1 = instructor_list[0:50]
	list_2 = instructor_list[50:]
	context = {
	'list_1': list_1,
	'list_2': list_2,
	}
	return render(request, 'recourse/instructor_list.html', context)

@login_required
def instructor_detail(request, instructor_id):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM recourse_instructors WHERE id = %s;", instructor_id)
	instructor = dictfetchall(cursor)
	if len(instructor)>0:
		instructor = instructor[0]
	else:
		raise Http404("Invalid instructor id.")

	cursor.execute("SELECT id, name FROM recourse_courses WHERE id IN (SELECT course_id FROM recourse_teach WHERE instructors_id = %s);", instructor_id)
	course_list = dictfetchall(cursor)
	context = {
	'instructor': instructor,
	'course_list': course_list
	}
	return render(request, 'recourse/instructor_details.html', context)

@login_required
def instructor_search(request):
	list = request.GET.get('instrName')
	list = '%' + list + '%'
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM recourse_instructors WHERE name LIKE %s;", list)
	instructor_list = dictfetchall(cursor)
	list_1 = instructor_list[0:len(instructor_list)/2]
	list_2 = instructor_list[len(instructor_list)/2:]
	context = {
	'list_1': list_1,
	'list_2': list_2,
	}
	return render(request, 'recourse/instructor_list.html', context)

# university
@login_required
def university_list(request):
	cursor = connection.cursor()
	cursor.execute("SELECT id, name FROM recourse_institutions ORDER BY id;")
	university_list = dictfetchall(cursor)
	context = {
	'university_list': university_list,
	}
	return render(request, 'recourse/university_list.html', context)

@login_required
def university_detail(request, university_id):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM recourse_institutions WHERE id = %s;", university_id)
	university = dictfetchall(cursor)
	if len(university)>0:
		university = university[0]
	else:
		raise Http404("Invalid university id.")

	cursor.execute("SELECT DISTINCT id, name FROM recourse_courses WHERE id IN (SELECT course_id FROM recourse_offer WHERE institution_id = %s);", university_id)
	course_list = dictfetchall(cursor)
	context = {
	'university': university,
	'course_list': course_list
	}
	return render(request, 'recourse/university_details.html', context)


# category
@login_required
def category_list(request, category_id):
	cursor = connection.cursor()
	pattern = ""
	if category_id == '1':
		pattern = "Arts-and-Humanities"
	elif category_id == '2':
		pattern = "Business"
	elif category_id == '3':
		pattern = "Computer-Science"
	elif category_id == '4':
		pattern = "Data-Science"
	elif category_id == '5':
		pattern = "Life-Sciences"
	elif category_id == '6':
		pattern = "Math-and-Logic"
	elif category_id == '7':
		pattern = "Personal-Development"
	elif category_id == '8':
		pattern = "Physical-Science-and-Engineering"
	elif category_id == '9':
		pattern = "Social-Sciences"
	elif category_id == '10':
		pattern = "Language-Learning"

	if pattern == "":
		course_list = []
	else:
		cursor.execute("SELECT DISTINCT recourse_courses.id, recourse_courses.name FROM recourse_courses, recourse_categories \
			WHERE recourse_courses.id = recourse_categories.course_id AND recourse_categories.category_name LIKE %s;", pattern)
		course_list = dictfetchall(cursor)

	context = {
	'course_list': course_list
	}
	return render(request, 'recourse/category.html', context)

def login_page(request):
	return render(request, 'recourse/login.html')

def user_login(request):
	if 'username_l' in request.POST:
		username = request.POST.get('username_l')
		password = request.POST.get('password_l')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return render(request, 'recourse/index.html')
		else:
			context = {
			'message': 'invalid username and password'
			}
			return render(request, 'recourse/login.html', context)

	elif 'username_r' in request.POST:
		username = request.POST.get('username_r')
		password = request.POST.get('password_r')
		email = request.POST.get('email_r')
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM auth_user WHERE username = %s;", username)
		user = dictfetchall(cursor)
		if len(user)>0:
			context = {
			'message': 'username already exist'
			}
			return render(request, 'recourse/login.html', context)
		else:
			context = {
			'message': 'create user successful'
			}
			user = User.objects.create_user(username, email, password)
			return render(request, 'recourse/login.html', context)

	else:
		return render(request, 'recourse/login.html')

@login_required
def user_logout(request):
	logout(request)
	context = {
		'message': 'logout successfully'
	}
	return render(request, 'recourse/login.html', context)

@login_required
def like_dislike(request):
	course_id = request.POST.get("course_id")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM recourse_like WHERE username = %s AND course_id = %s;", (request.user.username,course_id))
	likes = dictfetchall(cursor)
	if len(likes)>0:
		cursor.execute("DELETE FROM recourse_like WHERE username = %s AND course_id = %s;", (request.user.username,course_id))
		return HttpResponse("Like")
	else:
		cursor.execute("INSERT INTO recourse_like(username, course_id, time) VALUES (%s, %s, %s);", (request.user.username,course_id, datetime.date.today()))
		return HttpResponse("Dislike")

@login_required
def change_password(request):
	if 'password_n' in request.POST:
		n_password = request.POST.get('password_n')
		user = User.objects.get(username__exact=request.user.username)
		user.set_password(n_password)
		user.save()
		logout(request)
		context = {
			'message': 'change password successfully, please login again'
		}
		return render(request, 'recourse/login.html', context)
	else:
		return render(request, 'recourse/password_change.html')

#@login_required
