from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from todo.api import TodoItemResource


v1_api = Api(api_name='v1')
v1_api.register(TodoItemResource())


urlpatterns = patterns('',
    url(r'^$', 'todo.views.index', name='index'),
    url(r'^help$', 'todo.views.help', name='help'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
