from core.models import Semester, Person
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    list_display=('name', 'semester', 'lifetime', 'date_join')
    list_filter=['semester', 'lifetime', 'date_join']

class SemesterAdmin(admin.ModelAdmin):
    list_display=('name', 'start_date', 'end_date')

admin.site.register(Person, PersonAdmin)
admin.site.register(Semester, SemesterAdmin)
