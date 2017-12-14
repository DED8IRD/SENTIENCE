from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'shitposts'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^generate/', views.generate_post, name='generate')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
