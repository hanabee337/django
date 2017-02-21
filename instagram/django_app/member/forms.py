from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

from member.models import MyUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(max_length=30, required=False)
    gender = forms.ChoiceField(
        choices=MyUser.CHOICES_GENDER,
        widget=forms.RadioSelect(),
    )
    nickname = forms.CharField(max_length=30)

    def clean_username(self):
        """ username field 로직 검증 """
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError('username already exists')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        validate_password(password1)
        if password1 != password2:
            raise forms.ValidationError('password1 does not match')

        return password2

    def create_user(self):

        username = self.cleaned_data['username']
        password2 = self.cleaned_data['password2']
        email = self.cleaned_data['email']
        gender = self.cleaned_data['gender']
        nickname = self.cleaned_data['nickname']

        user = MyUser.objects.create_user(
            username=username,
            password=password2,
        )
        user.email = email
        user.gender = gender
        user.nickname = nickname
        user.save()
        return user


class SignupModelForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'gender',
            'nickname',
        )


class ProfileImageForm(forms.ModelForm):
    print('ProfileImageForm')

    class Meta:
        model = MyUser
        fields = (
            'img_profile',
        )
