from django.contrib.auth import forms as auth_forms
from django import forms
from django.core.files.uploadedfile import UploadedFile

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from web.models import AppUser, Mandate


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ('email', 'password')


# class UploadFileForm(forms.ModelForm):
#    class Meta:
#        model = UploadedFile
#        fields = ['file']


class MandateForm(forms.ModelForm):
    class Meta:
        model = Mandate
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
