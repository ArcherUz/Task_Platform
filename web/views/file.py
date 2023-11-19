from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.forms import model_to_dict
from web.forms.file import FolderModelForm
from web import models

import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError

from django.conf import settings

def file(request, project_id):
    parent_obj = None
    folder_id = request.GET.get('folder', "")
    if folder_id.isdecimal():
        parent_obj = models.FileRepository.objects.filter(id=int(folder_id), file_type=2, project=request.tracer.project).first()


    if request.method == 'GET':
        breadcrumb_list = []
        parent = parent_obj
        while parent:
            #breadcrumb_list.insert(0, {'id':parent.id, 'name':parent.name})
            breadcrumb_list.insert(0, model_to_dict(parent, ['id', 'name']))
            parent = parent.parent


        queryset = models.FileRepository.objects.filter(project=request.tracer.project)
        if parent_obj:
            file_object_list = queryset.filter(parent=parent_obj).order_by('-file_type')
        else:
            file_object_list = queryset.filter(parent__isnull=True).order_by('-file_type')

        form = FolderModelForm(request, parent_obj)
        context = {
            'form': form, 
            "file_object_list": file_object_list, 
            'breadcrumb_list': breadcrumb_list
        }
        return render(request, 'file.html', context)
    
    #POST
    fid = request.POST.get('fid', '')
    edit_obj = None
    if fid.isdecimal():
        edit_obj = models.FileRepository.objects.filter(id=int(fid), file_type=2, project=request.tracer.project).first()
    
    if edit_obj:
        form = FolderModelForm(request, parent_obj, data=request.POST, instance=edit_obj)
    else:
        form = FolderModelForm(request, parent_obj, data=request.POST)

    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_obj
        form.save()

        root_folder_name = f"{request.tracer.user.username}-{request.tracer.user.mobile_phone}/"
        if parent_obj:
            s3_folder_path = f"{root_folder_name}{form.instance.name}-{folder_id}/"
        else:
            s3_folder_path = f"{root_folder_name}{form.instance.name}/"
        #print(s3_folder_path)


        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                region_name = settings.AWS_S3_REGION_NAME,
            )
            s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_folder_path)
        except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)})

        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})

# localhost:8000/manage/1/file/delete/?fid=1
def file_delete(request, project_id):
    folder_id = request.GET.get('folder', "")
    fid=request.GET.get('fid')
    delete_obj = models.FileRepository.objects.filter(id=fid, project=request.tracer.project).first()
    if delete_obj.file_type == 1:
        file_key = f"{request.tracer.user.username}-{request.tracer.user.mobile_phone}/{delete_obj.name}"


        #delete file and return use_space
        request.tracer.project.user_space -= delete_obj.file_size
        request.tracer.project.save()

        #delete file in s3
        #pass after finished upload file

    else:
        if folder_id.isdecimal():
            s3_folder_path = f"{request.tracer.user.username}-{request.tracer.user.mobile_phone}/{delete_obj.name}-{folder_id}/"
        else:
            s3_folder_path = f"{request.tracer.user.username}-{request.tracer.user.mobile_phone}/{delete_obj.name}/"
        try:
            s3_resource = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            bucket = s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
            for obj in bucket.objects.filter(Prefix=s3_folder_path):
                obj.delete()
        except ClientError as e:
            return JsonResponse({'status': False, 'error': e})


    delete_obj.delete()
    return JsonResponse({'status': True})
    #return JsonResponse({'status': False, 'error': 'File/Folder not found'})