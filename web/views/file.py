from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.forms import model_to_dict
from web.forms.file import FolderModelForm
from web import models

import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError

from django.conf import settings

s3_client = boto3.client(
        's3',
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
        region_name = settings.AWS_S3_REGION_NAME,
    )

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

        
        for item in file_object_list:
            if item.file_type == 1:
                # Generate the presigned URL for file download
                try:
                    item.s3_presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': item.key})
                except ClientError as e:
                    item.s3_presigned_url = None

        form = FolderModelForm(request, parent_obj)
        context = {
            'form': form, 
            "file_object_list": file_object_list, 
            'breadcrumb_list': breadcrumb_list
        }
        return render(request, 'file.html', context)
    
    #POST add folder and change folder name
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

    if not delete_obj:
        return JsonResponse({'status': False, 'error': 'Object not found'})

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    total_size = 0
    s3_keys_to_delete = []

    if delete_obj.file_type == 1: #File
        #file_key = f"{request.tracer.user.username}-{request.tracer.user.mobile_phone}/{delete_obj.name}"
        file_key = f"{request.tracer.user.username}-{request.tracer.user.mobile_phone}/{delete_obj.id}-{delete_obj.name}"


        #delete file and return use_space
        request.tracer.project.use_space -= delete_obj.file_size
        request.tracer.project.save()

        try:
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
        except ClientError as e:
            return JsonResponse({'status': False, 'error': str(e)})

    else:
        folder_list = [delete_obj,]
        for folder in folder_list:
            child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by('-file_type') #first half is folder, second half is file
            for child in child_list:
                if child.file_type == 2:
                    folder_list.append(child)
                else: # file
                    total_size += child.file_size
                    file_key = f"{request.tracer.user.username}-{request.tracer.user.mobile_phone}/{child.id}-{child.name}"
                    s3_keys_to_delete.append(file_key)


    for key in s3_keys_to_delete:
        try:
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        except ClientError as e:
            return JsonResponse({'status': False, 'error': str(e)})
        
    if total_size:
        request.tracer.project.use_space -= total_size
        request.tracer.project.save()


    delete_obj.delete()
    return JsonResponse({'status': True})


def file_upload(request, project_id):
    
    if request.method == 'POST':
        folder_id = request.POST.get('folder', '')  # Get the folder ID from the URL
        parent_obj = None
        if folder_id.isdecimal():
            parent_obj = models.FileRepository.objects.filter(id=int(folder_id), file_type=2, project=request.tracer.project).first()

        file = request.FILES.get('fileUpload')
        if not file:
            return JsonResponse({'status': False, 'error': 'No file provided'})
        
        max_file_size = 1 * 1024 * 1024 #1MB
        if file.size > max_file_size:
            return JsonResponse({'status': False, 'error': 'File size exceeds limit'})
        
        file_instance = models.FileRepository.objects.create(
            project=request.tracer.project,
            file_type = 1,
            name=file.name,
            file_size=file.size,
            update_user=request.tracer.user,
            parent= parent_obj,

        )
        
        file_key = f"{request.tracer.user.username}-{request.tracer.user.mobile_phone}/{file_instance.id}-{file.name}"
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                region_name = settings.AWS_S3_REGION_NAME,
            )

            s3_client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_key)
        except Exception as e:
            file_instance.delete()
            return JsonResponse({'status': False, 'error': str(e)})
        
        file_instance.key = file_key
        file_instance.save()

        request.tracer.project.use_space += file_instance.file_size
        request.tracer.project.save()

        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': 'Invalid request'})

