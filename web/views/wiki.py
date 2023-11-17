from django.shortcuts import render, redirect, HttpResponse
from web.forms.wiki import WikiModelForm
from django.urls import reverse
from web import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
from django.conf import settings
from utils.encrypt import uid

def wiki(request, project_id):
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')
    
    wiki_obj = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
    return render(request, 'wiki.html', {'wiki_obj': wiki_obj})


def wiki_add(request, project_id):
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'wiki_form.html', {'form': form})
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.instance.project = request.tracer.project
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'wiki_form.html', {'form': form})

    
def wiki_catalog(request, project_id):
    data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id').order_by('depth', 'id')
    return JsonResponse({'status': True, 'data': list(data)})


def wiki_detail(request, project_id):
    return HttpResponse('wiki_detail')


def wiki_delete(request, project_id, wiki_id):
    models.Wiki.objects.filter(project_id=project_id, id=wiki_id).delete()
    url = reverse('wiki', kwargs={'project_id': project_id})
    return redirect(url)


def wiki_edit(request, project_id, wiki_id):
    wiki_obj = models.Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    if not wiki_obj:
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    if request.method == 'GET':
        form = WikiModelForm(request, instance=wiki_obj)
        return render(request, 'wiki_form.html', {'form': form})
    
    form = WikiModelForm(request, data=request.POST, instance=wiki_obj)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        preview_url = "{0}?wiki_id={1}".format(url, wiki_id)
        return redirect(preview_url)
    return render(request, 'wiki_form.html', {'form': form})

@csrf_exempt
def wiki_upload(request, project_id):
    image_obj = request.FILES.get('editormd-image-file')
    if image_obj:
        if image_obj.size > 1024 * 1024 * 2:
            return JsonResponse({'success': 0, 'message': "File size exceeds 2 MB limit"})
        
        ext = image_obj.name.rsplit('.')[-1]
        key = "{}.{}".format(uid(request.tracer.user.mobile_phone), ext)

        s3_client = boto3.client('s3',
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                region_name=settings.AWS_S3_REGION_NAME)
        
        file_path = f"upload/{key}"
        s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_path, Body=image_obj)
        file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_path}"
        success_result = {
            "success": 1,
            "message": "upload success",
            "url": file_url
        
        }
        return JsonResponse(success_result)
    return JsonResponse({"success": 0,"message": "No image to upload"})