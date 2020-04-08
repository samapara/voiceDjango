from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import AudioUploadModel, GenerateAudioRequestModel


class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioUploadModel
        fields = [
            'title',
            'audio'
        ]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class GenerateVoiceForm(forms.ModelForm):
    class Meta:
        model = GenerateAudioRequestModel
        fields = [
            'text',
            'audioName'
        ]