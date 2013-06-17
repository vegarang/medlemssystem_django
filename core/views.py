from django.shortcuts import render_to_response
from core.models import Person, Semester
from django.template import RequestContext
import datetime
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

def home(request):
    return render_to_response('core/home.html', context_instance=RequestContext(request))

def add(request):
    """
    reads name (required) and email (optional) from a POST-request, and creates a Person with the required fields.

    automatically locates or creates a Semester based on current date.

    If a person with the same parameters already exist, an error will be shown on add-page.
    """
    if not request.POST:
        return render_to_response('core/add.html', _get_newest_members(), context_instance=RequestContext(request))

    if not 'name' in request.POST or request.POST['name']=="":
        v = _get_newest_members()
        v['error']=True
        return render_to_response('core/add.html', v, context_instance=RequestContext(request))

    args={'lifetime':False, 'name':request.POST['name']}

    if 'email' in request.POST and request.POST['email']!="":
        args['email']=request.POST['email']

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
        v = _get_newest_members()
        v['info']=True
        return render_to_response('core/add.html', v, context_instance=RequestContext(request))
    return render_to_response('core/add.html', _get_newest_members(), context_instance=RequestContext(request))

def search(request):
    return render_to_response('core/search.html', context_instance=RequestContext(request))

def valid(request):
    return render_to_response('core/valid.html', context_instance=RequestContext(request))

def life(request):
    return render_to_response('core/life.html', context_instance=RequestContext(request))

def all(request):
    return render_to_response('core/all.html', context_instance=RequestContext(request))

def view(request):
    if not request.POST or not 'id' in request.POST:
        v = _get_newest_members()
        v['info']=True
        return render_to_response('core/add.html', v, context_instance=RequestContext(request))

    p=Person.objects.get(id=request.POST['id'])
    if 'delete' in request.POST and request.POST['delete']:
        return render_to_response('core/delete.html', {'person':p}, context_instance=RequestContext(request))

    if not 'name' in request.POST or not 'email' in request.POST or not 'lifetime' in request.POST:
        return render_to_response('core/view.html', {'person':p}, context_instance=RequestContext(request))

    p.name = request.POST['name']
    p.email = request.POST['email']
    p.lifetime = True if request.POST['name'] == 'y' else False

    p.save()

    v=_get_newest_members()
    v['success']=True
    return render_to_response('core/add.html', v, context_instance=RequestContext(request))

def delete(request):
    if not request.POST or not 'id' in request.POST:
        return render_to_response('core/add.html', {'error':True}, context_instance=RequestContext(request))

    p=Person.objects.get(id=request.POST['id'])
    p.delete()

    return render_to_response('core/add.html', {'success':True}, context_instance=RequestContext(request))

def test(request):
    return render_to_response('core_old/fluid.html', context_instance=RequestContext(request))

def _get_newest_members(numback=6):
    people=Person.objects.order_by('-date_join')[:numback]
    vals={}
    i=1
    for p in people:
        vals['sub{}'.format(i)]=p
        i+=1

    return vals

def makesemester():
    """
    make a new semester based on current date.
    spring: jan 1 -> jun 30
    fall: jul 1 -> dec 31
    """
    now=datetime.date.today()
    tmp=datetime.date(now.year, 7, 1)

    if now>=tmp:
        s=Semester.objects.create(name='h_{}'.format(now.year), start_date=tmp, end_date=datetime.date(now.year, 12, 31))
        return s

    s=Semester.objects.create(name='v_{}'.format(now.year), start_date=datetime.date(now.year, 1, 1), end_date=(tmp-datetime.timedelta(days=1)))
    return s

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def notes(request):
    return render_to_response('notes.html', context_instance=RequestContext(request))
