# Create your views here.
#from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from core.models import Person, Semester
from django.template import RequestContext
import datetime

def add_person(request):
    if request.POST:
        if not 'name' in request.POST or request.POST['name']=="":
            return render_to_response('core/add.html', {'fail':'no name in POST-data'}, context_instance=RequestContext(request))

        args={'name':request.POST['name']}
        if 'email' in request.POST and request.POST['email']!="":
            args['email']=request.POST['email']
        if 'life' in request.POST and request.POST['life']!="":
            args['lifetime']=request.POST['life']

        now=datetime.date.today()
        s=Semester.objects.filter(start_date__lte=now, end_date__gte=now)
        if len(s)==0:
            s=makesemester()
        else:
            s=s[0]
        args['semester']=s
        try:
            p=Person.objects.create(**args)
        except:
            return render_to_response('core/add.html', {'fail':'Database-error, most likely name is already added..'}, context_instance=RequestContext(request))

        return render_to_response('core/add.html', {'name':args['name']}, context_instance=RequestContext(request))

    return render_to_response('core/add.html', context_instance=RequestContext(request))

def list_person(request):
    gap=datetime.datetime.now()-datetime.timedelta(hours=12)
    people=Person.objects.all()
    current=people.filter(date_join__gte=gap)
    return render_to_response('core/list.html', {'people':people, 'total':len(people), 'current':len(current)}, context_instance=RequestContext(request))

def makesemester():
    now=datetime.date.today()
    tmp=datetime.date(now.year, 7, 1)

    if now>tmp:
        s=Semester.objects.create(name='h_{}'.format(now.year), start_date=tmp, end_date=datetime.date(now.year, 12, 31))
        return s

    s=Semester.objects.create(name='v_{}'.format(now.year), start_date=datetime.date(now.year, 1, 1), end_date=tmp)
    return s
