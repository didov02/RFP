from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Item, Pitch
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .forms import PostForm

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
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False) 
        post.from_user = request.user.username
        post.written_at = timezone.now()
        post.image = request.user.profile.image
        post.save()
        return redirect('RFP:start')
    else:
        print('Form not valid. Errors:', form.errors)
    
    return render(request, 'RFP_templates/addpost.html', {'form': form})