from django import forms


from .models import AudioUploadModel

class AudioUploadForm(forms.ModelForm):
	class Meta:
		model = AudioUploadModel
		fields = [
		'title',
		'audio'
		]
