from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import ProjectRequirement, WorkRecord, WorkRecordXProjectRequirement
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Max, Min
#from django.core.mail import send_mail
from postmarker.core import PostmarkClient
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
    print(request.user)
    project_id = 0
    project_title = "Title"
    if (request.POST):
        items = dict(request.POST.lists())
        print(items)
        project_id = items['sproject'][0]
        work_record_id = getNextWorkRecordID()
        with connection.cursor() as cursor:
            cursor.execute("insert into steeplechaser_workrecord (work_record_id, task_id, parent_task_id, status_cd, item_txt) select %s, task_id, parent_task_id, doable, item_txt from steeplechaser_projectrequirement where project_id = %s ",[work_record_id, project_id])
            cursor.execute("update steeplechaser_workrecord set status_cd = 'A' where work_record_id=%s and task_id=1",[work_record_id])
            wrxpr = WorkRecordXProjectRequirement(work_record_id=work_record_id, project_id=project_id, user_id=request.user.id)
            wrxpr.save()
    #task_listing = WorkRecord.objects.raw("select t1.work_record_id, t1.task_id, t1.parent_task_id, t1.status_cd, t1.item_txt from steeplechaser_workrecord t1, steeplechaser_workrecordxprojectrequirement wrxpr where t1.work_record_id = wrxpr.work_record_id and wrxpr.user_id='%s'",[request.user])
    task_listing = WorkRecord.objects.all().order_by('work_record_id','task_id')
    #task_listing = WorkRecord.objects.filter(work_record_id=work_record_id)
    template = loader.get_template('steeplechaser/notdone.html')
    context = {
        'task_listing' : task_listing
	
    }
    print("CONTEXTUNDONE: ", context)
    return HttpResponse(template.render(context, request))

def currentTask(request):
    template = loader.get_template('steeplechaser/current.html')
    # Need to filter to get current task for active user
    qset = WorkRecord.objects.filter(status_cd='A')
    if len(qset) > 0:
        wr = qset[0]
        parent_task_id = wr.parent_task_id
        task_id = wr.task_id
        pwr = WorkRecord.objects.filter(task_id=parent_task_id)[0]

        
        context = {
            'current_task' : task_id,
            'parent_task' : parent_task_id, 
            'work_record_id' : wr.work_record_id,
            'current_task_txt' : wr.item_txt,
            'parent_task_txt' : pwr.item_txt
        }
    else:
        context = {
            'alldone' : 1
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
        item_txt = items['newstep'][0]
        currentTask = WorkRecord.objects.filter(work_record_id=work_record_id, task_id=task_id)[0]
        print("CURRENTTASK",currentTask)
        print("TASKID", task_id, parent_task_id, work_record_id)
        if 'refine' in items.keys():
            newtask = WorkRecord(work_record_id=work_record_id,task_id=nextId,parent_task_id=task_id,status_cd="A",item_txt=item_txt)
            newtask.save()
            currentTask.status_cd="S"
            currentTask.save()
            print("Refining")
        if 'next' in items.keys():
            newtask = WorkRecord(work_record_id=work_record_id,task_id=nextId,parent_task_id=parent_task_id,status_cd="A",item_txt=item_txt)
            newtask.save()
            currentTask.status_cd="S"
            currentTask.save()
            print("Next")
        if 'complete' in items.keys():
            print("Complete")
            currentTask.status_cd="C"
            currentTask.save()
            current_task_id = currentTask.task_id
            nextTaskList = WorkRecord.objects.filter(work_record_id=currentTask.work_record_id, status_cd="S", task_id__gt=0).order_by('task_id') 
            if len(nextTaskList) > 0:
                nextTask = nextTaskList[0]
                nextTask.status_cd="A"
                nextTask.save()
		
            
        print("Next ID: ", nextId)
    template = loader.get_template('steeplechaser/basedone.html')
    context = { }
    return HttpResponse(template.render(context, request))

def remind(request):
    #send_mail('Steeplechaser Reminder Email','Here is the message','admin@steeplechaser.xyz',['markedup@gmail.com'])
    postmark = PostmarkClient(server_token='bb3a7634-2ec0-410d-9808-c39b4921af8c')
    postmark.emails.send(
        From='admin@steeplechaser.xyz',
        To='markedup@gmail.com',
        Subject='Steeplechaser Reminder',
        HtmlBody='<html><body><strong>Hello</strong> Remember your goal today!</body></html>')
    #hr = HttpRequest()
    #hr.method = 'POST'
    #hr.META['SERVER_NAME'] = 
    return HttpResponse("Hello, world. You're at steeplechaser.remind")
#def createWorkRecord(request):
#    template = loader.get_template('steeplechaser/creatework.html')
#
#    return 

