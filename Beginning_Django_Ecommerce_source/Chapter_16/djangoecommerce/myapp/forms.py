# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _, ugettext as __
from myapp.models import Person, File, Contract
from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets, FormSetField
from registration.forms import RegistrationForm, RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

class UserRegistrationForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^\w+$', max_length=30,
        label=_(u'Username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=75)),
         label=_(u'Email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'Password (again)'))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        user = User.get_by_key_name("key_"+self.cleaned_data['username'].lower())
        if user and user.is_active:
            raise forms.ValidationError(__(u'This username is already taken. Please choose another.'))
        return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(__(u'You must type the same password each time'))
        return self.cleaned_data
    
    def save(self, domain_override=""):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.
        
        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.
        
        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
            domain_override=domain_override)
        self.instance = new_user
        return super(UserRegistrationForm, self).save()

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        email = self.cleaned_data['email'].lower()
        if User.all().filter('email =', email).filter(
                'is_active =', True).count(1):
            raise forms.ValidationError(__(u'This email address is already in use. Please supply a different email address.'))
        return email

    class Meta:
        model = User
        exclude = UserTraits.properties().keys()

class FileForm(forms.ModelForm):
    name = forms.CharField(required=False, label='Name (set automatically)')

    def clean(self):
        file = self.cleaned_data.get('file')
        if not self.cleaned_data.get('name'):
            if isinstance(file, UploadedFile):
                self.cleaned_data['name'] = file.name
            else:
                del self.cleaned_data['name']
        return self.cleaned_data

    class Meta:
        model = File

class PersonForm(forms.ModelForm):
    files = FormSetField(File, form=FileForm, exclude='content_type')
    employers = FormSetField(Contract, fk_name='employee')
    employees = FormSetField(Contract, fk_name='employer')

    class Meta:
        model = Person
PersonForm = FormWithSets(PersonForm)
