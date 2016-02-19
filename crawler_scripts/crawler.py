import os
# get courses
'''
for i in range(0,19):
	command = "curl \"https://api.coursera.org/api/courses.v1?start=" + str(i*100) + "&fields=id,name,primaryLanguages,photoUrl,description,startDate,workload,previewLink,domainTypes,partnerIds,instructorIds&includes=instructorIds,partnerIds\" >" +  "courses_p" + str(i) + ".json"
	os.system(command)
	os.system("rm tmp.json")
	os.system("cat courses_p" + str(i) + ".json | python -m json.tool >> tmp.json")
	os.system("mv tmp.json courses_p" + str(i) + ".json")
	os.system("mv courses_p" + str(i) + ".json ./coursera_data/courses")

'''

# get instructors

for i in range(0,42):
	command = "curl \"https://api.coursera.org/api/instructors.v1?start=" + str(i*100) + "&fields=id,photo,bio,fullName,title,department,website&includes=universities,courses\" > instructors_p"  +  str(i) +".json"
	os.system(command)
	os.system("rm tmp.json")
	os.system("cat instructors_p" + str(i) + ".json | python -m json.tool >> tmp.json")
	os.system("mv tmp.json instructors_p" + str(i) + ".json")
	os.system("mv instructors_p" + str(i) + ".json ./coursera_data/instructors")

