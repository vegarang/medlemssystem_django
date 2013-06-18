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
    if not request.POST or not 'search' in request.POST or request.POST['search']=='':
        return render_to_response('core/search.html', context_instance=RequestContext(request))

    if 'all' in request.POST:
        return render_to_response('core/search.html',{'results':_get_all(request.POST['search'])}, context_instance=RequestContext(request))

    if 'valid' in request.POST:
        return render_to_response('core/search.html',{'results':_get_valid(request.POST['search'])}, context_instance=RequestContext(request))

    if 'life' in request.POST:
        return render_to_response('core/search.html',{'results':_get_life(request.POST['search'])}, context_instance=RequestContext(request))


def valid(request):
    args={
          'results':_get_valid(),
          'head':'All valid members!',
          'caption':' - kind of nice to know who they are, right?'
         }
    return render_to_response('core/list.html', args, context_instance=RequestContext(request))

def life(request):
    args={
          'results':_get_life(),
          'head':'Lifetime memberships!',
          'caption':' - So awesome that they get their own page!'
         }
    return render_to_response('core/list.html', args, context_instance=RequestContext(request))

def all(request):
    args={
          'results':_get_all(),
          'head':'All members!',
          'caption':' - because, why not?'
         }
    return render_to_response('core/list.html', args, context_instance=RequestContext(request))
    return render_to_response('core/list.html', context_instance=RequestContext(request))

def _get_valid(search=""):
    now=datetime.date.today()
    s=Semester.objects.filter(start_date__lte=now, end_date__gte=now)
    qs=Person.objects.filter(name__icontains=search, lifetime=True)
    if not len(s) == 0:
        s=s[0]
        qs1=Person.objects.filter(name__icontains=search, semester=s)
        qs=qs|qs1

    qs.order_by('-date_join')

    return qs

def _get_life(search=""):
    return Person.objects.filter(name__icontains=search, lifetime=True)

def _get_all(search=""):
    return Person.objects.filter(name__icontains=search)


def view(request):
    if request.POST and 'cancel' in request.POST:
        return render_to_response('core/add.html', _get_newest_members(), context_instance=RequestContext(request))

    if not request.POST or not 'id' in request.POST:
        v = _get_newest_members()
        v['error']=True
        return render_to_response('core/add.html', v, context_instance=RequestContext(request))

    p=Person.objects.get(id=request.POST['id'])
    if 'delete' in request.POST:
        return render_to_response('core/delete.html', {'person':p}, context_instance=RequestContext(request))

    if not 'name' in request.POST or not 'email' in request.POST:
        return render_to_response('core/view.html', {'person':p}, context_instance=RequestContext(request))

    p.name = request.POST['name']
    p.email = request.POST['email']
    p.lifetime = True if 'lifetime' in request.POST else False

    p.save()

    v=_get_newest_members()
    v['success']=True
    return render_to_response('core/add.html', v, context_instance=RequestContext(request))

def delete(request):
    if not request.POST or not 'id' in request.POST:
        v=_get_newest_members()
        v['error']=True
        return render_to_response('core/add.html', v, context_instance=RequestContext(request))

    if 'cancel' in request.POST or not 'confirm' in request.POST:
        return render_to_response('core/add.html', _get_newest_members(), context_instance=RequestContext(request))

    try:
        Person.objects.get(id=request.POST['id']).delete()
    except:
        v=_get_newest_members()
        v['error']=True
        return render_to_response('core/add.html', v, context_instance=RequestContext(request))


    v=_get_newest_members()
    v['success']=True
    return render_to_response('core/add.html', v, context_instance=RequestContext(request))

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
