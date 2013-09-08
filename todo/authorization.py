from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        if bundle.obj and bundle.obj.pk:
            return bundle.obj.user == bundle.request.user
        else:
            return True  # otherwise /schema doesn't work

    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no list creation.")

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no list updating.")

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no list deletion.")

    def delete_detail(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)
