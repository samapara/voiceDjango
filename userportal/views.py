import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets

from userportal.voice_backend.main import BackendHandler
from .forms import AudioUploadForm, CreateUserForm
from .models import AudioUploadModel, GeneratedAudioModel
# Create your views here.
from .serializers import UploadAudioSerializer


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = None
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account creation for ' + user + ' is successful !')
                return redirect('login')
            else:
                print(form.errors)

        context = {
            'form': form
        }
        return render(request, "userportal/register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, "userportal/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def audio_list(request):
    #    audio_list = AudioUploadModel.objects.all()
    my_audio_list = AudioUploadModel.objects.all().filter(username_ofaudiouploaded=request.user)
    # audio_list = my_model.objects.all()
    form = AudioUploadForm()
    context = {
        'audios': my_audio_list,
        'audioUploadForm': form
    }
    return render(request, 'audio_list.html', context)


@login_required(login_url='login')
def generated_list(request):
    my_audio_list = GeneratedAudioModel.objects.all().filter(username_ofaudiouploaded=request.user)
    username = request.user

    context = {
        'audios': my_audio_list,
    }
    return render(request, 'generated_audiolist.html', context)


def generate_audio(request):
    base_path = os.getcwd()
    if request.method == "POST":
        requestData = request.POST.dict()

        text = requestData["text"]
        audioName = requestData["audioName"]
        backendHandler = BackendHandler()
        audioPath = base_path + audioName
        print("Audio Path:", audioPath)

        backendHandler.test_models()

        processed_wav = backendHandler.process_audio_file(audioPath)

        voice_embedding = backendHandler.get_embedding(processed_wav)

        spectrogram = backendHandler.synthesize(text, voice_embedding)

        generated_wav = backendHandler.generate_wav(spectrogram)

        backendHandler.save_to_disk(generated_wav, base_path + "/media/audios/generated/test.wav")

        my_model = GeneratedAudioModel()

        reopen = open('media/audios/generated/test.wav', 'rb')
        django_file = File(reopen)

        my_model.audio = django_file
        my_model.audio.name = str(request.user) + ".wav"
        my_model.audioName = audioName
        my_model.text = text
        my_model.username_ofaudiouploaded = request.user
        my_model.save()

        return HttpResponse(201)

    return HttpResponse(400)


class UploadAudioViewSet(viewsets.ModelViewSet):
    queryset = AudioUploadModel.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadAudioSerializer


def indexPage(request):
    return render(request, 'index.html')
