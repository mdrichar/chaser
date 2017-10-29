from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import ProjectRequirement, WorkRecord, WorkRecordXProjectRequirement
from django.contrib.auth.models import User
from django.db import connection
import json

def index(request):
    return HttpResponse("Hello, world. You're at steeplechaser.index")


def startProject(request):
    template = loader.get_template('steeplechaser/start.html')

    project_listing = ProjectRequirement.objects.filter(task_id=1)
    #to_json = []
    #for project in project_listing:
    #    project_dict = {}
    #    project_dict['id'] = project.project_id
    #    project_dict['name'] = project.item_txt
    #    to_json.append(project_dict)
    #response_data = json.dumpts(to_json)
    context = {
        'project_listing' : project_listing
    }
    return HttpResponse(template.render(context, request))

def createWorkRecord(request):
    template = loader.get_template('steeplechaser/creatework.html')

    return 

