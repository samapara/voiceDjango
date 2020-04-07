from django.db import models

from .validators import validate_file_extension


# Create your models here.

class AudioUploadModel(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    audio = models.FileField(upload_to='audios/', validators=[validate_file_extension])

    def __str__(self):
        return self.title
