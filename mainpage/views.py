from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Item, Pitch, BoughtItem
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import PostForm
from .additional_functions import generate_random_code
from django.contrib.auth.models import User
from users.forms import ProfileForm
from users.models import Profile
from users.models import FriendRequest

# Create your views here.
@login_required
def start(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'RFP_templates/index.html', context)

@login_required
def reserve_pitch(request):
    pitches = Pitch.objects.all()
    context = {
        'pitches' : pitches,
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'RFP_templates/reservepitch.html', context)

@login_required
def friends(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'RFP_templates/friends.html', context)

@login_required
def send_requests(request):
    current_user = request.user
    current_user_profile = Profile.objects.get(user=current_user)
    friend_requests = request.user.profile.received_friend_requests.all()

    senders = []

    for friend_request in friend_requests:
        senders.append(friend_request.sender)

    all_users = User.objects.exclude(pk=current_user.id)
    
    users_not_friends = []

    for user in all_users:
        if user.profile not in current_user_profile.friends.all() and user not in senders:
            users_not_friends.append(user)

    return render(request, 'RFP_templates/sendrequest.html', {'not_friends': users_not_friends})

@login_required
def send_request(request, id):
    current_user = request.user
    sender= current_user
    receiver=User.objects.get(pk=id)

    friend_request = FriendRequest.objects.create(
        sender=sender,
        receiver=receiver,
    )

    receiver_profile = Profile.objects.get(user=receiver)
    receiver_profile.received_friend_requests.add(friend_request)

    current_user_profile = Profile.objects.get(user=current_user)

    all_users = User.objects.exclude(pk=current_user.id).exclude(pk=id)
    
    users_not_friends = []

    for user in all_users:
        if user.profile not in current_user_profile.friends.all():
            users_not_friends.append(user)

    return render(request, 'RFP_templates/sendrequest.html', {'not_friends':users_not_friends})

@login_required
def see_friends_request(request):
    friend_requests = request.user.profile.received_friend_requests.all()

    senders = []

    for friend_request in friend_requests:
        senders.append(friend_request.sender)

    return render(request, 'RFP_templates/seefriendrequests.html', {'senders': senders})

@login_required
def accept_request(request, id):
    current_user = request.user
    sender = User.objects.get(pk=id)

    friend_request = get_object_or_404(FriendRequest, id=id, receiver=current_user)
    friend_request.delete()

    current_user.profile.friends.add(sender.profile)
    
    return redirect('RFP:friends')
    

@login_required
def shop(request):
    items = Item.objects.all()
    context = {
        'items' : items
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'RFP_templates/shop.html', context)

@login_required
def settings(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['email'] = request.user.email

    return render(request, 'RFP_templates/settings.html', context) 

@login_required
def detail(request, id):
    pitch = Pitch.objects.get(pk=id)
    context = {
        'pitch':pitch,
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username

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

@login_required
def buy_item(request, id):
    item = Item.objects.get(pk=id)
    item_price = int(request.GET['price'])
    
    if request.user.profile.tokens - item_price >= 0:
        request.user.profile.tokens -= item_price
        request.user.profile.save()

        BoughtItem.objects.create(
            item_name=item,
            item_code = generate_random_code(),
            bought_from=request.user
        )

    return redirect('RFP:bought_items')

@login_required
def bought_items(request):
    bought_items = BoughtItem.objects.filter(bought_from=request.user)
    return render(request, 'RFP_templates/boughtitems.html', {'bought_items': bought_items})

@login_required
def see_reserved_pitches(request):
    request.user.profile.tokens = request.user.profile.tokens + 1
    request.user.profile.save()

    return redirect('RFP:start')

@login_required
def personal_info(request, id):
    user = User.objects.get(pk=id)
    return render(request, 'RFP_templates/personalinfo.html', {'user' : user})

@login_required
def change_info(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_profile.age = form.cleaned_data['age']
            user_profile.city = form.cleaned_data['city']
            user_profile.position = form.cleaned_data['position']
            user_profile.image = form.cleaned_data['image']
            user_profile.save()
            return redirect('RFP:start')
    else:
        form = ProfileForm(initial={
            'age': user_profile.age,
            'city': user_profile.city,
            'position': user_profile.position,
            'image': user_profile.image,
        })

    return render(request, 'RFP_templates/changepersonalinfo.html', {'form': form})

@login_required
def view_friends(request):
    current_user = request.user
    friends_list = current_user.profile.friends.all()

    return render(request, 'RFP_templates/viewfriends.html', {'friends_list': friends_list})
    