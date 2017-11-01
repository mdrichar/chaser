
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
        url(r'^start$', views.startProject, name='startProject'),
        url(r'^undone$', views.undone, name='undone'),
        url(r'^current$', views.currentTask, name='currentTask'),
        url(r'^nexttodo$', views.nextToDo, name='nexttodo'),
        url(r'^remind$', views.remind, name='remind'),      
        #url(r'^done$', views.done, name='done'),      
]
