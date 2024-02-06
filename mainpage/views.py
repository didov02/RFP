from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Item, Pitch
from django.template import loader
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def start(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }

    if request.user.is_authenticated:
        context.update({'username': request.user.username})

    return render(request, 'RFP_templates/index.html', context)

@login_required
def reserve_pitch(request):
    pitches = Pitch.objects.all()
    context = {
        'pitches' : pitches,
    }

    if request.user.is_authenticated:
        context.update({'username': request.user.username})

    return render(request, 'RFP_templates/reservepitch.html', context)

@login_required
def friends(request):
    context = {

    }

    if request.user.is_authenticated:
        context.update({'username': request.user.username})

    return render(request, 'RFP_templates/friends.html', context)

@login_required
def add_friend(request):
    return HttpResponse('Here you can add friends')

@login_required
def shop(request):
    items = Item.objects.all()
    context = {
        'items' : items
    }

    if request.user.is_authenticated:
        context.update({'username': request.user.username})

    return render(request, 'RFP_templates/shop.html', context)

@login_required
def settings(request):
    context = {

    }

    if request.user.is_authenticated:
        context.update({'username': request.user.username, 'email': request.user.email})

    return render(request, 'RFP_templates/settings.html', context) 

@login_required
def detail(request, id):
    pitch = Pitch.objects.get(pk=id)
    context = {
        'pitch':pitch,
    }

    if request.user.is_authenticated:
        context.update({'username': request.user.username})

    return render(request, 'RFP_templates/detail.html', context)

@login_required
def add_post(request):
    if request.method == 'POST':
        from_user = request.POST.get('from_user')
        written_at = request.POST.get('written_at')
        message = request.POST.get('message')

        Post.objects.create(from_user=from_user, written_at=written_at, message=message)

        return redirect('RFP_templates/index.html')
    else:
        return render(request, 'RFP_templates/index.html')