from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .models import Pitch
from django.template import loader

# Create your views here.
def start(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }
    return render(request, 'RFP_templates/index.html', context)

def reserve_pitch(request):
    pitches = Pitch.objects.all()
    context = {
        'pitches' : pitches,
    }
    return render(request, 'RFP_templates/reservepitch.html', context)

def friends(request):
    return HttpResponse('This is the friends menu')

def add_friend(request):
    return HttpResponse('Here you can add friends')

def shop(request):
    return HttpResponse('This is the shop menu')

def settings(request):
    context = {

    }
    return render(request, 'RFP_templates/settings.html', context) 

def detail(request, id):
    pitch = Pitch.objects.get(pk=id)
    context = {
        'pitch':pitch,
    }
    return render(request, 'RFP_templates/detail.html', context)