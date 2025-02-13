from django import forms
from .models import Subscriber

class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'aria-label': 'Email address for newsletter',
            'required': True,
            'autocomplete': 'email'
        })
    )

    class Meta:
        model = Subscriber
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already subscribed to our newsletter.')
        return email