from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm mt-1 block w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm mt-1 block w-full'}),
            'email': forms.EmailInput(attrs={'class': 'form-input rounded-md shadow-sm mt-1 block w-full'}),
        }
