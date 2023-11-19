'''Register, Login, SMS, Logout'''
import uuid
import datetime
import boto3
from botocore.exceptions import NoCredentialsError

from django.shortcuts import render, HttpResponse, redirect
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from django.http import JsonResponse
from django.conf import settings

from web import models
from web.models import UserInfo

def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        instance = form.save()

        policy_price = models.PricePolicy.objects.filter(category=1, title='Free').first()
        models.Transaction.objects.create(
            status=2,
            order= str(uuid.uuid4()),
            user = instance,
            price_policy = policy_price,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now(),
        )

        #s3 directory create username-phone number

        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                region_name = settings.AWS_S3_REGION_NAME,
            )
            folder_name = f"{instance.username}-{instance.mobile_phone}/"
            s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=folder_name)
        except NoCredentialsError:
            return JsonResponse({'status': False, 'error': 'AWS credentials not available'})

        return JsonResponse({'status': True, 'data':'/login/'})
    return JsonResponse({'status': False, 'error': form.errors})
    

def send_sms(request):
    #mobile_phone = request.GET.get('mobile_phone')

    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def login_sms(request):
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})
    
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        #user_obj = form.cleaned_data['mobile_phone']
        mobile_phone = form.cleaned_data['mobile_phone']
        user_obj = UserInfo.objects.filter(mobile_phone=mobile_phone).first()

        request.session['user_id'] = user_obj.id
        request.session.set_expiry(60*60*24*14)

        return JsonResponse({'status': True, 'data':'/index/'})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        #user_obj = UserInfo.objects.filter(username=username, password=password).first()
        from django.db.models import Q
        user_obj = UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(password=password).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60*60*24*14)
            return redirect('index')
        
        
        form.add_error('username', 'Username or password error')
    
    return render(request, 'login.html', {'form': form})

def image_code(request):
    from utils.image_code import check_code
    from io import BytesIO
    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)
    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('index')
