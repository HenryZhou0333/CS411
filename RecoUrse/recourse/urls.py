from django.conf.urls import url

from . import views
##

app_name = 'recourse'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^course_(?P<course_id>.+)/$', views.course_detail, name='course_detail'),
	url(r'^courseQuery/$', views.course_search, name='course_search'),
	url(r'^ListInstructor/$', views.instructor_list, name='instructor_list'),
	url(r'^instructor_(?P<instructor_id>.+)/$', views.instructor_detail, name='instructor_detail'),
	url(r'^instructorQuery/$', views.instructor_search, name='instructor_search'),
	url(r'^ListUniversity/$', views.university_list, name='university_list'),
	url(r'^university_(?P<university_id>.+)/$', views.university_detail, name='university_detail'),
	url(r'^ListCategory_(?P<category_id>[0-9]+)/$', views.category_list, name='category_list'),
	url(r'^login_page/$', views.login_page, name='login_page'),
	url(r'^user_login/$', views.user_login, name='user_login'),
	url(r'^user_logout/$',views.user_logout, name='user_logout'),
	url(r'^like_dislike/$', views.like_dislike, name='like_dislike'),
	url(r'^change_password/$', views.change_password, name='change_password'),
]
