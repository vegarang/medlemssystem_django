# Create your views here.
#from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from core.models import Person, Semester
from django.template import RequestContext
import datetime
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

def delete_person(request):
    """
    Takes a POST-request with name (required) and email (optional), locates the person that matches, and deletes it. If no person is found, or multiple
    people are found, an error will be returned.

    if the argument 'check' is found in the POST-request, then a site asking if you are sure you want to delete is shown instead.
    """
    if not request.POST:
        return render_to_response('core/delete.html', context_instance=RequestContext(request))

    if not 'name' in request.POST or request.POST['name']=="":
        return render_to_response('core/add.html', {'fail':'Delete failed! No name in POST-data'}, context_instance=RequestContext(request))

    args={'name':request.POST['name']}
    if 'email' in request.POST:
        args['email']=request.POST['email']

    try:
        p=Person.objects.get(**args)
    except MultipleObjectsReturned:
        return render_to_response('core/add.html', {'fail':'Delete failed! Multiple people match search'}, context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        return render_to_response('core/add.html', {'fail':'Delete failed! Person not found..'}, context_instance=RequestContext(request))

    if 'check' in request.POST:
        return render_to_response('core/delete.html', {'person':p}, context_instance=RequestContext(request))

    p.delete()
    return render_to_response('core/add.html', {'removed':request.POST['name']}, context_instance=RequestContext(request))

def add_person(request):
    """
    reads name (required) email (optional) and lifetime(optional) from a POST-request, and creates a Person with the required fields.

    automatically locates or creates a Semester based on current date.

    If a person with the same parameters already exist, an error will be shown on add-page.
    """
    if not request.POST:
        return render_to_response('core/add.html', context_instance=RequestContext(request))

    if 'info' in request.POST:
        return render_to_response('core/add.html', {'info':request.POST['info']})

    if not 'name' in request.POST or request.POST['name']=="":
        return render_to_response('core/add.html', {'fail':'no name in POST-data'}, context_instance=RequestContext(request))

    args={'name':request.POST['name']}
    if 'email' in request.POST and request.POST['email']!="":
        args['email']=request.POST['email']

    if 'life' in request.POST and request.POST['life']!="":
        args['lifetime']=True if request.POST['life'] == 'life' else False

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

def edit_person(request):
    """
    locates a person based on name and email in POST, and updates it with values new_name, new_email and life from POST.

    error is shown if new_name == "" or an error occures when saving.
    """
    if not 'name' in request.POST:
        return render_to_response('core/add.html', {'fail':'Cannot find person to edit.'}, context_instance=RequestContext(request))

    p=Person.objects.get(name=request.POST['name'], email=request.POST['email'])

    if not 'save' in request.POST:
        life = 'life' if p.lifetime else 'single'
        return render_to_response('core/edit.html', {'person':p, 'membership':life}, context_instance=RequestContext(request))

    if request.POST['new_name'] == "":
        return render_to_response('core/add.html', {'fail':'Edit failed! Cannot save person with no name..'}, context_instance=RequestContext(request))

    p.name=request.POST['new_name']
    p.email=request.POST['new_email']
    p.lifetime=True if request.POST['life'] == "life" else False

    try:
        p.save()
    except:
        return render_to_response('core/add.html', {'fail':'Database-error, most likely name already exists..'}, context_instance=RequestContext(request))
    return render_to_response('core/add.html', {'name':p.name}, context_instance=RequestContext(request))


def list_person(request):
    """
    lists all people, and gives info on how many members last 12 hours, and how many lifetime members.
    """
    gap=datetime.datetime.now()-datetime.timedelta(hours=12)
    people=Person.objects.all()
    lifetime=len(people.filter(lifetime=True))
    current=len(people.filter(date_join__gte=gap))
    return render_to_response('core/list.html', {'people':people, 'total':len(people), 'num_cur':current, 'num_life':lifetime, 'headline':'All members'}, context_instance=RequestContext(request))

def list_current(request):
    """
    same as list_person, but only lists people who are members this semester, or are lifetime members.
    """
    gap=datetime.datetime.now()-datetime.timedelta(hours=12)
    now=datetime.date.today()
    s=Semester.objects.filter(start_date__lte=now, end_date__gte=now)[0]
    people=Person.objects.all().exclude(lifetime=False, date_join__lte=s.start_date)
    lifetime=len(people.filter(lifetime=True))
    current=len(people.filter(date_join__gte=gap))
    return render_to_response('core/list.html', {'people':people, 'total':len(people), 'num_cur':current, 'num_life':lifetime, 'headline':'All members'}, context_instance=RequestContext(request))

def list_lifetime(request):
    """
    lists only lifetime members
    """
    people=Person.objects.filter(lifetime=True)
    return render_to_response('core/list.html', {'people':people, 'total':len(people), 'headline':'Lifetime members'}, context_instance=RequestContext(request))

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

def index(request):
    """
    show main page
    """
    return render_to_response('core/index.html')

def search(request):
    """
    return a list of all people matching name in POST.

    if membership is in post, and POST[membership] is 'lifetime' only lifetime members will be searched.
    """
    if not request.POST:
        return render_to_response('core/search.html', {}, context_instance=RequestContext(request))

    people=Person.objects.filter(name__icontains=request.POST['name'])

    if not 'membership' in request.POST or request.POST['membership'] == 'all':
        now=datetime.date.today()
        s=Semester.objects.filter(start_date__lte=now, end_date__gte=now)[0]
        people=people.exclude(lifetime=False, date_join__lte=s.start_date)
        return render_to_response('core/list.html', {'people':people, 'headline':'Search-results for: '.format(request.POST['name']), 'origin':'search'}, context_instance=RequestContext(request))
    people=people.filter(lifetime=True)
    return render_to_response('core/list.html', {'people':people, 'headline':'Search-results for: '.format(request.POST['name']), 'origin':'search'}, context_instance=RequestContext(request))
