import django
django.setup()
from steeplechaser.models import ProjectRequirement, WorkRecord, WorkRecordXProjectRequirement


def build():
    for i in range(5):
        pr = ProjectRequirement(project_id=i, task_id=0, parent_task_id=0, prefix=str(i) + '.', item_txt="Project " + str(i), doable='S')
        pr.save()
        for j in range(1,6):
            pr = ProjectRequirement(project_id=i, task_id=j, parent_task_id=0, prefix=str(i) + '.', item_txt="Do requirement " + str(j), doable='S')
            pr.save()

for p in ProjectRequirement.objects.all():
    print(p)

def build2():
    pr = ProjectRequirement(project_id=1, task_id=0, parent_task_id=0, prefix="", item_txt="Citizenship in the Community", doable='D')
    pr.save()
    pr = ProjectRequirement(project_id=2, task_id=0, parent_task_id=0, prefix="", item_txt="Citizenship in the World", doable='D')
    pr.save()
    pr = ProjectRequirement(project_id=3, task_id=0, parent_task_id=0, prefix="", item_txt="Citizenship in the Nation", doable='D')
    pr.save()
    pr = ProjectRequirement(project_id=3, task_id=1, parent_task_id=0, prefix="1.", item_txt="Explain what citizenship means and what it takes to be a good citizen of this country. Discuss the rights, duties, and obligations of a responsible and active American citizen", doable='S')
    pr.save()
    pr = ProjectRequirement(project_id=3, task_id=2, parent_task_id=0, prefix="2.", item_txt="Do TWO of the following:", doable='D')
    pr.save()
    pr = ProjectRequirement(project_id=3, task_id=3, parent_task_id=2, prefix="a.", item_txt="Visit a place that is listed as a National Historic Landmark or that is on the National Registry of Historic Places. Tell your counselor what you learned about the landmark or site and what you found interesting about it.", doable='S')
    pr.save()
    pr = ProjectRequirement(project_id=3, task_id=4, parent_task_id=2, prefix="b.", item_txt="Tour your state capitol building or the U.S. Capitol. Tell your counselor what you learned about the capitol, its function, and the history.", doable='S')
    pr.save()
    pr = ProjectRequirement(project_id=3, task_id=5, parent_task_id=2, prefix="c.", item_txt="Tour a federal facility. Explain to your counselor what you saw there and what you learned about its function in the local community and how it serves this nation.", doable='S')
    pr.save()
    pr = ProjectRequirement(project_id=3, task_id=6, parent_task_id=2, prefix="d.", item_txt="Choose a national monument that interests you. Using books, brochures, the Internet (with your parent's permission), and other resources, find out more about the monument. Tell your counselor what you learned, and explain why the monument is important to this country's citizens.", doable='S')
    pr.save()
    pr = ProjectRequirement(project_id=3, task_id=7, parent_task_id=0, prefix="3.", item_txt="Watch the national evening news five days in a row OR read the front page of a major daily newspaper five days in a row. Discuss the national issues you learned about with your counselor. Choose one of the issues and explainhow it affects you and your family.", doable='S')
    pr.save()
    pr = ProjectRequirement(project_id=4, task_id=0, parent_task_id=0, prefix="", item_txt="Programming", doable='D')
    pr.save()
    pr = ProjectRequirement(project_id=5, task_id=0, parent_task_id=0, prefix="", item_txt="Wood Badge Ticket", doable='D')
    pr.save()
    pr = ProjectRequirement(project_id=6, task_id=0, parent_task_id=0, prefix="", item_txt="First Aid", doable='D')
    pr.save()
    pr = ProjectRequirement(project_id=7, task_id=0, parent_task_id=0, prefix="", item_txt="Emergency Preparedness", doable='D')
    pr.save()
    
    pr.save()

def destroy():
    ProjectRequirement.objects.all().delete()
    WorkRecord.objects.all().delete()
    WorkRecordXProjectRequirement.objects.all().delete()
    for p in ProjectRequirement.objects.all():
        print(p)


destroy()
build2()
