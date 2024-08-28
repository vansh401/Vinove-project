from django.http import HttpResponse
from .tasks import start_services
from django.shortcuts import render

def home(request):

    return render(request, 'index.html')

