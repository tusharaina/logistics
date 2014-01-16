from django import forms
from .models import Manifest


class UploadManifestForm(forms.ModelForm):

    class Meta:
        model = Manifest
        exclude = ['status', 'is_active', 'uploaded_by', 'branch']


