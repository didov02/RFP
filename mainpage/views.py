from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Item, Pitch
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
    context = {

    }
    return render(request, 'RFP_templates/friends.html', context)

def add_friend(request):
    return HttpResponse('Here you can add friends')

def shop(request):
    items = Item.objects.all()
    context = {
        'items' : items
    }
    return render(request, 'RFP_templates/shop.html', context)

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

def add_post(request):
    if request.method == 'POST':
        from_user = request.POST.get('from_user')
        written_at = request.POST.get('written_at')
        message = request.POST.get('message')

        Post.objects.create(from_user=from_user, written_at=written_at, message=message)

        return redirect('RFP_templates/index.html')
    else:
        return render(request, 'RFP_templates/index.html')