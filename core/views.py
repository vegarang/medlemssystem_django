# Create your views here.
from django.http import Http404, HttpResponse
from core.models import Person, Semester
import json
from django.shortcuts import render_to_response

def get_people(request):
    """
    Return all :class:`people<core.models.Person>` in database as JSON
    """
    qs=Person.objects.all()

    people=[]

    for p in qs:
        people.append(p.to_dict())

    js=json.dumps(people)
    return HttpResponse(js)

def get_lifetime(request):
    """
    Return all :class:`people<core.models.Person>` with ``lifetime=True`` as JSON
    """
    qs=Person.objects.filter(lifetime=True)

    people=[]

    for p in qs:
        people.append(p.to_dict())

    js=json.dumps(people)
    return HttpResponse(js)

def get_semesters(request):
    """
    Return basic info on all :class:`semesters<core.models.Semester>` in database as JSON
    """
    qs=Semester.objects.all()

    semesters=[]

    for s in qs:
        semesters.append(s.to_dict())

    js=json.dumps(semesters)
    return HttpResponse(js)

def get_people_by_semester(request, semester):
    """
    Return one :class:`semester<core.models.Semester>` based on ``name`` with all linked
    :class:`people<core.models.Person>` in database as JSON
    """
    try:
        s=Semester.objects.get(name=semester)
    except Semester.DoesNotExist:
        raise Http404

    js=json.dumps(s.to_dict_full())
    return HttpResponse(js)

def test(request):
    return HttpResponse(open('core/static/main.js', 'r').read(), content_type='application/javascript')
    #return render_to_response('core/static/main.html')
