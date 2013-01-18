# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from core.models import Person, Semester
from django.template import RequestContext
import datetime

def add_person(request):
    if request.POST:
        now=datetime.date.today()
        s=Semester.objects.filter(start_date__lte=now, end_date__gte=now)
        if len(s)==0:
            s=makesemester()
        else:
            s=s[0]
        p=Person.objects.create(semester=s, name=request.POST['name'], email=request.POST['email'], lifetime=request.POST['life'])
        return render_to_response('core/add.html', {'name':request.POST['name']}, context_instance=RequestContext(request))

    return render_to_response('core/add.html', context_instance=RequestContext(request))

def list_person(request):
    return render_to_response('core/list.html', {'people':Person.objects.all()}, context_instance=RequestContext(request))

def makesemester():
    now=datetime.date.today()
    tmp=datetime.date(now.year, 7, 1)

    if now>tmp:
        s=Semester.objects.create(name='h_{}'.format(now.year), start_date=tmp, end_date=datetime.date(now.year, 12, 31))
        return s

    s=Semester.objects.create(name='v_{}'.format(now.year), start_date=datetime.date(now.year, 1, 1), end_date=tmp)
    return s
