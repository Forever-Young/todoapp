import json
import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

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
        return None
    return _dumpjson(list(TodoItem.objects.filter(user=request.user).values()))


def index(request):
    data = {
        "data": get_todolist(request),
        "available_priorities": json.dumps([' '] + [i[0] for i in TodoItem._meta.get_field_by_name("priority")[0].choices]),
    }
    return render_to_response("index.html", data, context_instance=RequestContext(request))

@login_required()
def help(request):
    data = {
        "apikey": request.user.api_key.key,
    }
    return render_to_response("help.html", data, context_instance=RequestContext(request))
