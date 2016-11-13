from django import forms
from django.contrib.auth.models import User
from grumblr.models import UserProfile


class RegistrationForm(forms.ModelForm):
    confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email')
        widgets = {'password' : forms.PasswordInput}

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        if not cleaned_data.get('first_name'):
            raise forms.ValidationError("first name required.")

        if not cleaned_data.get('last_name'):
            raise forms.ValidationError("last name required.")

        if not cleaned_data.get('email'):
            raise forms.ValidationError("email required.")

        if User.objects.filter(username=cleaned_data.get("username")).count() > 0:
            raise forms.ValidationError("user name already exists.")

        if cleaned_data.get('password') != cleaned_data.get('confirm'):
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user', 'following',)
        widgets = { 'photo' : forms.FileInput(),
                    'change_pwd' : forms.PasswordInput,
                    'confirm' : forms.PasswordInput,

        }

    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()

        password = cleaned_data.get('change_pwd')
        con = cleaned_data.get('confirm')
        if (password or con) and password != con:
            raise forms.ValidationError("Password does not match.")

        return cleaned_data
