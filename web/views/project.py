from django.shortcuts import render, redirect, HttpResponse
from web.forms.project import ProjectModelForm
from django.http import JsonResponse
from web import models

def project_list(request):
    if request.method == 'GET':
        form = ProjectModelForm(request)

        project_dict = {'star':[], 'my':[], 'join':[]}

        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append({'value':row, 'type':'my'})
            else:
                project_dict['my'].append(row)
        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value':item.project, 'type':'join'})
            else:
                project_dict['join'].append(item.project)

        return render(request,'project_list.html', {'form': form, 'project_dict': project_dict})
    
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        form.instance.creator = request.tracer.user
        form.save()


        return JsonResponse({'status': True})
    
    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('project_list')
    
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('project_list')
    
def project_unstar(request, project_type, project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('project_list')
    
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('project_list')