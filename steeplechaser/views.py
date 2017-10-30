from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import ProjectRequirement, WorkRecord, WorkRecordXProjectRequirement
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Max
import json

def index(request):
    return HttpResponse("Hello, world. You're at steeplechaser.index")


def startProject(request):
    template = loader.get_template('steeplechaser/start.html')

    project_listing = ProjectRequirement.objects.filter(task_id=0)
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
    print("CONTEXT: ", context)
    return HttpResponse(template.render(context, request))

def getNextWorkRecordID():
    return 2

def getNextTaskId():
    try:
        max_id = 1 + WorkRecord.objects.all().aggregate(Max('task_id'))['task_id__max']
    except:
        max_id = 1
    return max_id
    

def undone(request):
    project_id = 0
    project_title = "Title"
    if (request.POST):
        items = dict(request.POST.lists())
        print(items)
        project_id = items['sproject'][0]
        work_record_id = getNextWorkRecordID()
        with connection.cursor() as cursor:
            cursor.execute("insert into steeplechaser_workrecord (work_record_id, task_id, parent_task_id, status_cd, item_txt) select %s, task_id, parent_task_id, 'I', item_txt from steeplechaser_projectrequirement where project_id = %s",[work_record_id, project_id])
            cursor.execute("update steeplechaser_workrecord set status_cd = 'A' where work_record_id=%s and task_id=1",[work_record_id])
    task_listing = WorkRecord.objects.filter(work_record_id=work_record_id)
    template = loader.get_template('steeplechaser/notdone.html')
    context = {
        'work_record_id' : work_record_id,
        'task_listing' : task_listing
	
    }
    print("CONTEXTUNDONE: ", context)
    return HttpResponse(template.render(context, request))

def currentTask(request):
    template = loader.get_template('steeplechaser/current.html')
    context = {
        'current_task' : 1,
        'parent_task' :0, 
        'work_record_id' :2
    }
    return HttpResponse(template.render(context, request))

def nextToDo(request):
    if (request.POST):
        items = dict(request.POST.lists())
        print(items)
        nextId = getNextTaskId()
        task_id = int(items['current_task'][0])
        parent_task_id = int(items['parent_task'][0])
        work_record_id = int(items['work_record_id'][0])
        currentTask = WorkRecord.objects.filter(work_record_id=work_record_id, task_id=task_id)[0]
        print("CURRENTTASK",currentTask)
        print("TASKID", task_id, parent_task_id, work_record_id)
        if 'refine' in items.keys():
            newtask = WorkRecord(work_record_id=work_record_id,task_id=nextId,parent_task_id=task_id,status_cd="A",item_txt="Default")
            newtask.save()
            currentTask.status_cd="I"
            currentTask.save()
            print("Refining")
        if 'next' in items.keys():
            newtask = WorkRecord(work_record_id=work_record_id,task_id=nextId,parent_task_id=parent_task_id,status_cd="A",item_txt="Default")
            currentTask.status_cd="I"
            currentTask.save()
            print("Next")
        if 'complete' in items.keys():
            print("Complete")
            currentTask.status_cd="C"
            currentTask.save()
        print("Next ID: ", nextId)
    return HttpResponse("Hello, world. You're at steeplechaser.nexttodo")

#def createWorkRecord(request):
#    template = loader.get_template('steeplechaser/creatework.html')
#
#    return 

