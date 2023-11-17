from django.template import Library
from web import models
from django.urls import reverse

register = Library()

@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    my_project_list = models.Project.objects.filter(creator=request.tracer.user)

    join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)

    return {'my': my_project_list, 'join': join_project_list, 'request': request}

@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    data_list = [
        {'title': 'Dashboard', 'url': reverse('dashboard', kwargs={'project_id': request.tracer.project.id})},
        {'title': 'Issues', 'url': reverse('issues', kwargs={'project_id': request.tracer.project.id})},
        {'title': 'Wiki', 'url': reverse('wiki', kwargs={'project_id': request.tracer.project.id})},
        {'title': 'Statistics', 'url': reverse('statistics', kwargs={'project_id': request.tracer.project.id})},
        {'title': 'Setting', 'url': reverse('setting', kwargs={'project_id': request.tracer.project.id})},
        {'title': 'File', 'url': reverse('file', kwargs={'project_id': request.tracer.project.id})},
        
    ]
    
    for item in data_list:
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'
        
    return {'data_list': data_list}