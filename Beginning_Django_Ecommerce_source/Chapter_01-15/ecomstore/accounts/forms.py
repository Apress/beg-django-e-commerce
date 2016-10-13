from django import forms
from django.contrib.auth.forms import UserCreationForm
from ecomstore.accounts.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        
class RegistrationForm(UserCreationForm):
    """ subclass of Django's UserCreationForm, to handle customer registration with a required minimum length
    and password strength. Also contains an additional field for capturing the email on registration.
    
    """
    password1 = forms.RegexField(label="Password", regex=r'^(?=.*\W+).*$', 
                                 help_text='Password must be six characters long and contain at least one non-alphanumeric character.',
                                 widget=forms.PasswordInput, min_length=6)
    password2 = forms.RegexField(label="Password confirmation", regex=r'^(?=.*\W+).*$',
                                 widget=forms.PasswordInput, min_length=6)
    email = forms.EmailField(max_length="50")