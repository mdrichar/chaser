import django
django.setup()
from steeplechaser.models import ProjectRequirement


def build():
    for i in range(5):
        pr = ProjectRequirement(project_id=i, task_id=0, parent_task_id=0, prefix=str(i) + '.', item_txt="Project " + str(i), doable='S')
        pr.save()
        for j in range(1,6):
            pr = ProjectRequirement(project_id=i, task_id=j, parent_task_id=0, prefix=str(i) + '.', item_txt="Do requirement " + str(j), doable='S')
            pr.save()

for p in ProjectRequirement.objects.all():
    print(p)

ProjectRequirement.objects.all().delete()

def destroy():
    for p in ProjectRequirement.objects.all():
        print(p)


destroy()
build()
