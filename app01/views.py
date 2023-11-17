from django.shortcuts import render, HttpResponse
from utils.SMS.twilio_sms import send_sms
from app01 import models
from django import forms
from django.core.validators import RegexValidator

# Create your views here.
def send_sms_view(request):
    res = send_sms(target='+17807076732', content='Your verification code is: ')
    return HttpResponse(res)

class RegisterModelForm(forms.ModelForm):
    phone = forms.CharField(label='Phone_number',widget=forms.TextInput( attrs={'placeholder': '+17777777777'}), validators=[RegexValidator(r'^\+1\d{10}$', 'Phone number format error')])
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm_password', widget=forms.PasswordInput())
    code = forms.CharField(label='Verification code', widget=forms.TextInput(attrs={'placeholder': 'Verification code'}))

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password','phone', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

def register_view(request):
    form = RegisterModelForm()
    return render(request, 'app01/register.html', {'form': form})