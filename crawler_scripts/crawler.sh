cd ./coursera_data

# get courses
rm courses.json

curl "https://api.coursera.org/api/courses.v1?fields=id,name,primaryLanguages,photoUrl,description,startDate,workload,previewLink,domainTypes,partnerIds,instructorIds&includes=instructorIds,partnerIds" > courses.json
cat courses.json | python -m json.tool >> courses2.json
rm courses.json
mv courses2.json courses.json


# get instructors

#rm instructors.json
#curl "https://api.coursera.org/api/instructors.v1?fields=id,photo,bio,fullName,title,department,website&includes=universities,courses" > instructors.json
#cat instructors.json | python -m json.tool >> instructors2.json
#rm instructors.json
#mv instructors2.json instructors.json


# get partners

#rm partners.json
#curl "https://api.coursera.org/api/partners.v1?fields=id,name,description,banner,courseIds,instructorIds,links,location&includes=courseIds,instructorIds" > partners.json
#cat partners.json | python -m json.tool >> partners2.json
#rm partners.json
#mv partners2.json partners.json

