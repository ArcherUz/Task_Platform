
from django.urls import path, include
from web.views import account
from web.views import home
from web.views import project
from web.views import manage
from web.views import wiki

from web.views import file

manage_patterns = [
        path('dashboard/', manage.dashboard, name='dashboard'),
        path('issues/', manage.issues, name='issues'),
        path('statistics/', manage.statistics, name='statistics'),
        
        path('wiki/', wiki.wiki, name='wiki'),
        path('wiki/add/', wiki.wiki_add, name='wiki_add'),
        path('wiki/catalog/', wiki.wiki_catalog, name='wiki_catalog'),
        path('wiki/delete/<int:wiki_id>/', wiki.wiki_delete, name='wiki_delete'),
        path('wiki/edit/<int:wiki_id>/', wiki.wiki_edit, name='wiki_edit'),
        path('wiki/upload/', wiki.wiki_upload, name='wiki_upload'),

        path('file/', file.file, name='file'),
        path('file/delete/', file.file_delete, name='file_delete'),
        path('file/upload/', file.file_upload, name='file_upload'),
        path('setting/', manage.setting, name='setting'),
    ]


urlpatterns = [
    path('register/', account.register, name='register'),
    path('login/sms/',account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('image/code/', account.image_code, name='image_code'),

    path('send/sms/', account.send_sms, name='send_sms'),
    path('logout/', account.logout, name='logout'),

    path('index/', home.index, name='index'),

    path('project/list/', project.project_list, name='project_list'),
    path('project/star/<str:project_type>/<int:project_id>/', project.project_star, name='project_star'),
    path('project/unstar/<str:project_type>/<int:project_id>/', project.project_unstar, name='project_unstar'),

    path('manage/<int:project_id>/', include(manage_patterns)),
]
