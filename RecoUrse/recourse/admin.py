from django.contrib import admin

# Register your models here.
from .models import Courses,Categories,Instructors,Institutions,Users,Like,Teach,Offer

admin.site.register(Courses)
admin.site.register(Categories)
admin.site.register(Instructors)
admin.site.register(Institutions)
admin.site.register(Users)
admin.site.register(Like)
admin.site.register(Teach)
admin.site.register(Offer)