from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from clock.models import Record, Project


class RecordAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Record, RecordAdmin)
admin.site.register(Project, ProjectAdmin)
