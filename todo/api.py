from tastypie.constants import ALL
from tastypie.resources import ModelResource
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, SessionAuthentication
from .authorization import UserObjectsOnlyAuthorization
from .models import TodoItem


class TodoItemResource(ModelResource):
    def __init__(self, **kwargs):
        super(TodoItemResource, self).__init__(**kwargs)
        self.fields["id"].readonly = True

    class Meta:
        queryset = TodoItem.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'delete']
        resource_name = 'todo'
        excludes = ['user']
        ordering = ['due', 'priority']
        filtering = {'completed': ALL, 'text': ALL}
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = UserObjectsOnlyAuthorization()

    def obj_create(self, bundle, **kwargs):
        return super(TodoItemResource, self).obj_create(bundle, user=bundle.request.user)
