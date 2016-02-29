from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from .models import Courses,Instructors,Institutions,Users,Like,Teach,Offer
from django.db import connection

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Create your views here.
def index(request):
	return render(request, 'recourse/index.html')

# courses
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

def course_detail(request, course_id):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM recourse_courses WHERE id = %s;", course_id)
	course = dictfetchall(cursor)
	if len(course)>0:
		course = course[0]
	else:
		raise Http404("Invalid course id.")
	context = {
	'course': course,
	}
	return render(request, 'recourse/course_details.html', context)


# instructor
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
def university_list(request):
	cursor = connection.cursor()
	cursor.execute("SELECT id, name FROM recourse_institutions ORDER BY id;")
	university_list = dictfetchall(cursor)
	context = {
	'university_list': university_list,
	}
	return render(request, 'recourse/university_list.html', context)


def university_detail(request, university_id):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM recourse_institutions WHERE id = %s;", university_id)
	university = dictfetchall(cursor)
	if len(university)>0:
		university = university[0]
	else:
		raise Http404("Invalid university id.")
	
	cursor.execute("SELECT id, name FROM recourse_courses WHERE id IN (SELECT course_id FROM recourse_offer WHERE institution_id = %s);", university_id)
	course_list = dictfetchall(cursor)
	context = {
	'university': university,
	'course_list': course_list
	}
	return render(request, 'recourse/university_details.html', context)



# category
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
		cursor.execute("SELECT recourse_courses.id, recourse_courses.name FROM recourse_courses, recourse_categories \
			WHERE recourse_courses.id = recourse_categories.course_id AND recourse_categories.category_name LIKE %s;", pattern)
		course_list = dictfetchall(cursor)

	context = {
	'course_list': course_list
	}
	return render(request, 'recourse/category.html', context)