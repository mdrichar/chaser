from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProjectRequirement(models.Model):
    project_id = models.IntegerField(default=0)
    task_id = models.IntegerField(default=0)
    parent_task_id = models.IntegerField(default=0)
    prefix = models.CharField(max_length=20)
    item_txt = models.CharField(max_length=2048)
    doable = models.CharField(max_length=20)

    def __str__(self):
        return '(' + str(self.project_id) + "," + str(self.task_id) + "," + str(self.parent_task_id) + "," + self.prefix + "," + self.item_txt + "," + self.doable + ")"

class WorkRecord(models.Model):
    work_record_id = models.IntegerField(default=0)
    task_id = models.IntegerField(default=0)
    parent_task_id = models.IntegerField(default=0)
    item_txt = models.CharField(max_length=2048)
    status_cd = models.CharField(max_length=20)

    def __str__(self):
        return '(' + str(self.work_record_id) + "," + str(self.task_id) + "," + str(self.parent_task_id) + "," + self.status_cd + "," + self.item_txt + ")"

class WorkRecordXProjectRequirement(models.Model):
    work_record_id = models.IntegerField(default=0)
    project_id = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return '(' + str(self.work_record_id) + ',' + str(self.project_id) + ',' + self.user_id + ')'
    	

