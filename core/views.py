from django.shortcuts import render_to_response
from core.models import Person, Semester
from django.template import RequestContext
import datetime
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

def home(request):
    return render_to_response('core/home.html', context_instance=RequestContext(request))

def add(request):
    return render_to_response('core/add.html', context_instance=RequestContext(request))

def search(request):
    return render_to_response('core/search.html', context_instance=RequestContext(request))

def valid(request):
    return render_to_response('core/valid.html', context_instance=RequestContext(request))

def life(request):
    return render_to_response('core/life.html', context_instance=RequestContext(request))

def all(request):
    return render_to_response('core/all.html', context_instance=RequestContext(request))

def view(request):
    return render_to_response('core/view.html', context_instance=RequestContext(request))

def test(request):
    return render_to_response('core_old/fluid.html', context_instance=RequestContext(request))
