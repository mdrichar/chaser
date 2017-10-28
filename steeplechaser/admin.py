from django.contrib import admin

from .models import ProjectRequirement, WorkRecord, WorkRecordXProjectRequirement

# Register your models here.

admin.site.register(ProjectRequirement)
admin.site.register(WorkRecord)
admin.site.register(WorkRecordXProjectRequirement)
