from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from .forms import AudioUploadForm
from .models import AudioUploadModel

# Create your views here.

def indexPage(request):

	if request.method=='POST':
		form=AudioUploadForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/audio_list')
	else:
		form=AudioUploadForm()
	context={
		'form' : form
	}
	return render(request,'index.html',context)

def audio_list(request):
	audio_list = AudioUploadModel.objects.all()
	context={
	'audios' : audio_list
	} 
	return render(request,'audio_list.html',context)


	