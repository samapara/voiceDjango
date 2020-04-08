from django.contrib import admin

from .models import AudioUploadModel as AudioModel
from .models import GenerateAudioRequestModel

# Register your models here.from django.contrib import admin

admin.site.register(AudioModel)
admin.site.register(GenerateAudioRequestModel)
