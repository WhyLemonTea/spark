from django import forms
from django.core.exceptions import ValidationError
import re
import datetime
from book.models import BookUser

def check_phone(phone):
    phone_re = re.match(r'^1[2345678]\d{9}$', phone)
    if phone_re:
        return True
    else:
        raise ValidationError('手机号码格式有误')

def check_borthday(birthday):
    ch_birth = datetime.datetime.strptime(str(birthday), '%Y-%m-%d').date()
    if ch_birth and '1910-01-01' < str(birthday) < str(
            datetime.datetime.today().strftime('%y-%m-%d')):
        return True
    else:
        raise ValidationError('生日不合法')


def check_pwd(pwd):
    ch_pwd = re.match(r'(?=.*[A-Za-z0-9\D._])(?=.*[A-Z])(?=.*[a-z]).{6,20}', pwd)
    if not ch_pwd:
        raise ValidationError('密码复杂度不够')


class Req_From(forms.Form):
    username = forms.CharField(label='用户名', required=True, max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}),
                               error_messages={
                                   'required': '必需的',
                                   'max_length': '用户名太长'
                               })
    pwd = forms.CharField(label='密码', required=True, min_length=6, max_length=20, validators=[check_pwd],
                          widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
                          error_messages={
                              'required': '必需的',
                              'max_length': '最大20位',
                              'min_length': '最小6位',
                              'validators': '密码复杂度不够'
                          })
    pwd1 = forms.CharField(label='重复密码', required=True, min_length=6, max_length=20, validators=[check_pwd],
                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}),
                           error_messages=dict(required='必需的', max_length='最大20位', min_length='最小6位',
                                               validators='密码复杂度不够'))

    phone = forms.CharField(label='电话号码', required=True, min_length=11, max_length=11, validators=[check_phone],
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请电话号码'}),
                            error_messages=dict(required='必需的', max_length='11位号码', min_length='11位号码',
                                                validators='电话号码不合法'))

    gender = forms.ChoiceField(label='性别', required=True, choices=((0, '女'), (1, '男'), (2, '未知')), initial=2,
                               widget=forms.RadioSelect())

    birthday = forms.DateField(label='生日', required=True, validators=[check_borthday],
                               widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                               error_messages=dict(required='必需的', validators='生日不合法'))


    def clean_username(self):
        user = self.cleaned_data.get('username')
        user1=BookUser.objects.filter(username=user)
        if user1.count() >= 1:
            raise ValidationError('此用户已存在')
        if user == '666':
            raise ValidationError('此用户不能注册')
        return user

    def clean_gender(self):
        gender=self.cleaned_data.get('gender')
        if int(gender) not in [0,1,2]:
            raise ValidationError('性别不合法')
        return int(gender)
    def clean(self):
        pwdd=self.cleaned_data
        pwd=pwdd.get('pwd')
        pwd1=pwdd.get('pwd1')
        if pwd!=pwd1:
            raise ValidationError('两次密码不一致')
        return pwdd