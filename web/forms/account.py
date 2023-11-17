from django import forms
from django.core.validators import RegexValidator
from web.models import UserInfo
import random
from utils.SMS.twilio_sms import send_sms
from utils.encrypt import md5

from django_redis import get_redis_connection

from web.forms.bootstrap import BootStrapForm




class RegisterModelForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    mobile_phone = forms.CharField(label='Phone number',widget=forms.TextInput( attrs={'placeholder': '+17777777777'}), validators=[RegexValidator(r'^\+1\d{10}$', 'Phone number format error')])
    code = forms.CharField(label='Verification code', widget=forms.TextInput(attrs={'placeholder': 'Verification code'}))

    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'password', 'confirm_password','mobile_phone', 'code']


    def clean_username(self):
        username = self.cleaned_data['username']
        exists = UserInfo.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('Username already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = UserInfo.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('Email already exists')
        return email
    
    def clean_password(self):
        pwd = self.cleaned_data['password']

        return md5(pwd)
    
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise forms.ValidationError('Two passwords are inconsistent')
        return confirm_pwd
    
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise forms.ValidationError('The phone number already exists.')
        return mobile_phone
    
    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise forms.ValidationError('Verification code has expired or does not exist')
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise forms.ValidationError('Verification code error')
        return code


    

class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='Phone_number', widget=forms.TextInput(attrs={'placeholder': '+17777777777'}), validators=[RegexValidator(r'^\+1\d{10}$', 'Phone number format error')])
    
    def __init__(self,request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        tpl = self.request.GET.get('tpl')
        if tpl == 'login':
            if not exists:
                raise forms.ValidationError('This phone number is not registered')
        else:                
            if exists:
                raise forms.ValidationError('This phone number is already registered')
        
        code = random.randrange(1000,9999)
        res = send_sms(mobile_phone, code)
        if res == 'Phone type error':
            raise forms.ValidationError('Phone type error')
        
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60)

        
        return mobile_phone
    

class LoginSMSForm(BootStrapForm, forms.Form):
    mobile_phone = forms.CharField(
        label='Phone number',
        widget=forms.TextInput( attrs={'placeholder': '+17777777777'}), 
        validators=[RegexValidator(r'^\+1\d{10}$', 'Phone number format error')]
    )

    code = forms.CharField(
        label='Verification code', 
        widget=forms.TextInput(attrs={'placeholder': 'Verification code'})
    )

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        #user_obj = UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not exists:
            raise forms.ValidationError('This phone number is not registered')
        return mobile_phone
    
    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone.mobile_phone)

        if not redis_code:
            raise forms.ValidationError('Verification code has expired or does not exist')
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise forms.ValidationError('Verification code error')
        
        return code
    

class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='Email or Phone Number', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    code = forms.CharField(label='Verification code', widget=forms.TextInput(attrs={'placeholder': 'Verification code'}))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)

    def clean_code(self):
        code = self.cleaned_data['code']
        session_code = self.request.session['image_code']
        if not session_code:
            raise forms.ValidationError('Please refresh the verification code')
        if code.strip().upper() != session_code.strip().upper():
            raise forms.ValidationError('Verification code error')
        return code