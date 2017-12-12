from django.conf.urls import url
from . import views

app_name = 'shitposts'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<shitpost_id>[0-9]+)/$', views.detail, name='detail'),
]