from django.shortcuts import render


# Create your views here.

def indexPage(req):
    return render(req, 'index.html', {'name':'Shubham'})
