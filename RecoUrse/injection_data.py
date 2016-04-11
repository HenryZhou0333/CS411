import os
os.environ['DJANGO_SETTINGS_MODULE']='RecoUrse.settings'
import re
import django
django.setup()
from recourse.models import Courses,Categories,Instructors,Institutions,Users,Like,Teach,Offer,Similar

def remove_html_tags(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)

def inject_courses():
	for i in range(0,19):
		name = "../coursera_data/courses/courses_p" + str(i) + ".json"
		splice = open(name, "r")
		content = eval(splice.read())["elements"]
		for j in range(0,len(content)):
			element = content[j]
			_id = element["id"]
			_name = element["name"] if ("name" in element) else "" 
			_description = remove_html_tags(element["description"]) if ("description" in element) else "" 
			_language = element["primaryLanguages"] if ("primaryLanguages" in element) else ""
			_photo = element["photoUrl"] if ("photoUrl" in element) else ""
			_workload = element["workload"] if ("workload" in element) else ""
			_previewLink = element["previewLink"] if ("previewLink" in element) else ""
			obj = Courses(id=_id,name=_name,description=_description,language=_language,photo=_photo,workload=_workload,previewLink=_previewLink)
			obj.save()


def inject_instructors():
	for i in range(0,42):
		name = "../coursera_data/instructors/instructors_p" + str(i) + ".json"
		splice = open(name, "r")
		content = eval(splice.read())["elements"]
		for j in range(0, len(content)):
			element = content[j]
			_id = (int)(element["id"])
			_name = element["fullName"] if ("fullName" in element) else "" 
			_bio = remove_html_tags(element["bio"]) if ("bio" in element) else ""
			_photo = element["photo"] if ("photo" in element) else ""
			_title = element["title"] if ("title" in element) else ""
			_website = element["website"] if ("website" in element) else ""
			_department = element["department"] if ("department" in element) else ""
			obj = Instructors(id=_id,name=_name,bio=_bio,photo=_photo,title=_title,website=_website,department=_department)
			obj.save()


def inject_institutions():
	name = "../coursera_data/partners.json"
	splice = open(name, "r")
	content = eval(splice.read())["elements"]
	for j in range(0, len(content)):
		element = content[j]
		_id = element["id"]
		_name = element["name"] if ("name" in element) else "" 
		_description = remove_html_tags(element["description"]) if ("description" in element) else ""
		_links = element["links"] if ("links" in element) else {}
		_location = element["location"] if ("location" in element) else {}
		obj = Institutions(id=_id,name=_name,description=_description,links=_links,location=_location)
		obj.save()

def inject_teach():
	for i in range(0,19):
		name = "../coursera_data/courses/courses_p" + str(i) + ".json"
		splice = open(name, "r")
		content = eval(splice.read())["elements"]
		for j in range(0,len(content)):
			element = content[j]
			_instructorIds = element["instructorIds"]
			_course_id = element["id"]
			for k in range(0, len(_instructorIds)):
				_instructor_id = (int)(_instructorIds[k])
				obj = Teach(instructors_id=_instructor_id,course_id=_course_id)
				obj.save()
				

def inject_offer():
	for i in range(0,19):
		name = "../coursera_data/courses/courses_p" + str(i) + ".json"
		splice = open(name, "r")
		content = eval(splice.read())["elements"]
		for j in range(0,len(content)):
			element = content[j]
			_partnerIds = element["partnerIds"]
			_course_id = element["id"]
			for k in range(0, len(_partnerIds)):
				_partner_id = _partnerIds[k]
				obj = Offer(institution_id=_partner_id, course_id=_course_id)
				obj.save()

def inject_categories():
	for i in range(0,19):
		name = "../coursera_data/courses/courses_p" + str(i) + ".json"
		splice = open(name, "r")
		content = eval(splice.read())["elements"]
		for j in range(0,len(content)):
			element = content[j]
			_domainTypes = element["domainTypes"]
			_course_id = element["id"]
			for k in range(0, len(_domainTypes)):
				_domain_type = _domainTypes[k]["domainId"]
				obj = Categories(category_name=_domain_type, course_id=_course_id)
				obj.save()


def inject_similar():
	name = "../coursera_data/similar"
	file_ = open(name, "r")
	line = file_.readline()
	while(line!=""):
		words = line.split()
		obj = Similar(course1_id = words[0], course2_id = words[1])
		obj.save()
		line = file_.readline()


_type = (int)(raw_input("what to inject what data? (1--courses, 2--instructors, 3--institutions, 4--teach, 5--offer, 6--categories, 7--similar_courses, 8--user, 9--like, )\n"))
if _type==1:
	inject_courses()
elif _type==2:
	inject_instructors()
elif _type==3:
	inject_institutions()
elif _type==4:
	inject_teach()
elif _type==5:
	inject_offer()
elif _type==6:
	inject_categories()
elif _type==7:
	inject_similar()
#else:
#


