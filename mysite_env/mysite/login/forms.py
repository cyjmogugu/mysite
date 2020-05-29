#-*- codeing=uft-8 -*-
#@Time: 2020/5/18 22:30
#@Author:陈怡婧
#@File ：forms.py
#@Software:PyCharm

from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class new_register_form(UserCreationForm):#自定义注册表单
    昵称=forms.CharField(required=False,max_length=50)
    生日=forms.DateField(required=False)
    captcha=CaptchaField()
    class Meta:
        model=User
        fields=('username','password1','password2','email','昵称','生日')

class new_edit_form(UserChangeForm):#自定义编辑表单
    昵称=forms.CharField(required=False,max_length=50)
    生日=forms.DateField(required=False)

    class Meta:
        model=User
        fields=('username','password','email','昵称','生日')

class captcha_form(forms.Form):
    captcha = CaptchaField(label='验证码',
        required=True,
        error_messages={
            'required': '验证码不能为空'
        })