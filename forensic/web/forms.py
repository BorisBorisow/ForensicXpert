from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.db import transaction
from web.models import AppUser, Mandate, Client, Employee, ContactPerson


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ('email', 'password')


class AppUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = '__all__'


class ClientSingUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=512)
    last_name = forms.CharField(max_length=512)
    title = forms.CharField(max_length=512, required=False)
    institution_free = forms.CharField(max_length=512)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ["email", "password"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_client = True
        user.save()
        ContactPerson.objects.create(
            user=user,
            title=self.cleaned_data.get("title"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            institution_free=self.cleaned_data.get("institution_free"),
        )
        return user


class EmployeeSingUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = AppUser
        fields = ["email", "password"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_staff = True
        user.set_password(self.cleaned_data["password"])
        user.save()
        Employee.objects.create(
            user=user,
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
        )
        return user


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        # fields = ['first_name', 'last_name', 'mobile', 'profile_picture']
        fields = "__all__"


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = "__all__"


# class UploadFileForm(forms.ModelForm):
#    class Meta:
#        model = UploadedFile
#        fields = ['file']


class MandateForm(forms.ModelForm):
    class Meta:
        model = Mandate
        fields = "__all__"


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super(MandateForm, self).__init__(*args, **kwargs)
    #     # Add placeholders to form fields
    #     self.fields['mandate_number'].widget.attrs['placeholder'] = 'Enter mandate number'
    #     self.fields['denotation'].widget.attrs['placeholder'] = 'Enter mandate denotation'
    #     self.fields['date_mandate_received'].widget.attrs['placeholder'] = 'Enter received data'
    #     self.fields['details'].widget.attrs['placeholder'] = 'Enter mandate details'
    #     self.fields['description'].widget.attrs['placeholder'] = 'Enter mandate description'
    #     self.fields['comments'].widget.attrs['placeholder'] = 'Enter mandate comments'
    #     self.fields['priority'].widget.attrs['placeholder'] = 'Enter mandate priority'
    #     self.fields['client'].widget.attrs['placeholder'] = 'Enter client'
    #     self.fields['client_contact'].widget.attrs['placeholder'] = 'Enter client_contact'
    #     self.fields['investigation_group'].widget.attrs['placeholder'] = 'Enter investigation_group'
    #     self.fields['investigation_group_contact'].widget.attrs['placeholder'] = 'Enter investigation_group_contact'
