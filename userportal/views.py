from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import AudioUploadForm, CreateUserForm
from .models import AudioUploadModel


# Create your views here.
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
    audio_list = AudioUploadModel.objects.all()
    context = {
        'audios': audio_list
    }
    return render(request, 'audio_list.html', context)


@login_required(login_url='login')
def indexPage(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/audio_list')
    else:
        form = AudioUploadForm()
    context = {
        'form': form
    }
    return render(request, 'index.html', context)
