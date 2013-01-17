from django.db import models

class Semester(models.Model):
    """
    Database-field to store a semester.

    Contains:

        * a semesters name, eg 'Spring 2013'
        * a semesters start-date
        * a semesters end-date


    The combination of name, start_date and end_date is unique
    """
    name=models.CharField(max_length=15)
    start_date=models.DateField()
    end_date=models.DateField()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together=('name', 'start_date', 'end_date')

    def to_dict(self):
        retval={}
        retval['start_date']=self.start_date.strftime('%Y-%m-%d')
        retval['end_date']=self.end_date.strftime('%Y-%m-%d')
        retval['name']=self.name

        return retval

    def to_dict_full(self):
        retval=self.to_dict()
        people=[]
        for p in Person.objects.filter(semester=self):
            people.append(p.to_dict())

        retval['people']=people
        return retval

class Person(models.Model):
    """
    Database-field to store a person.

    Contains:

        * a persons name
        * datetime when the person was registered
        * the semester in question.

    Name is unique for each semester.
    """
    name=models.CharField(max_length=40)
    date_join=models.DateTimeField(auto_now=True)
    semester=models.ForeignKey(Semester)
    lifetime=models.BooleanField()

    def to_dict(self):
        retval={}
        retval['name']=self.name
        retval['date_join']=self.date_join.strftime('%Y-%m-%d %H:%M:%S')
        retval['lifetime']=self.lifetime

        return retval

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together=('name', 'semester', 'lifetime')
