import json
import datetime
import math

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import TodoItem


class _DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return super(_DateTimeJSONEncoder, self).default(obj)


def _dumpjson(data):
    return json.dumps(data, cls=_DateTimeJSONEncoder)


def get_todolist(request):
    if not request.user.is_authenticated():
        return None, 0
    queryset = TodoItem.objects.filter(user=request.user)
    length = int(math.ceil(len(queryset) / float(settings.PAGINATOR_ITEMS_PER_PAGE)))
    return _dumpjson(list(queryset.values())[:settings.PAGINATOR_ITEMS_PER_PAGE]), length


def index(request):
    lst, pages = get_todolist(request)
    data = {
        "data": lst,
        "max_pages": pages,
        "items_per_page": settings.PAGINATOR_ITEMS_PER_PAGE,
        "available_priorities": json.dumps([' '] + [i[0] for i in TodoItem._meta.get_field_by_name("priority")[0].choices]),
    }
    return render_to_response("index.html", data, context_instance=RequestContext(request))


@login_required()
def help(request):
    data = {
        "apikey": request.user.api_key.key,
    }
    return render_to_response("help.html", data, context_instance=RequestContext(request))
