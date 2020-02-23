from django import forms
from paster.models import Paste
from django.contrib.auth.models import User

class PasteForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(PasteForm,self).__init__(*args,**kwargs)
        #Add form-control class for all the fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Paste
        fields = ['title','content','syntax','expiry']

class SignUpForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': 'Passwords did not match',
        'email_already_taken': 'Email has been taken already'
    }

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        #Add form-control class for all the fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError(
                self.error_messages['email_already_taken']
            )


    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self,*args,**kwargs):
        super(LoginForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
