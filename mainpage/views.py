from django.shortcuts import render, redirect
from .models import Post, Item, Pitch, BoughtItem, Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import ReservationForm
from .additional_functions import generate_random_code
from django.contrib.auth.models import User
from users.forms import ProfileForm
from users.models import Profile
from users.models import FriendRequest
from django.contrib import messages

# Create your views here.
@login_required
def start(request):
    posts = Post.objects.all()
    context = {}
    current_user = request.user

    if request.user.is_authenticated:
        context['user'] = current_user

    friends = current_user.profile.friends.all()
    friends_usernames = [friend.user.username for friend in friends]
    posts_from_friends = []

    for post in posts:
        if post.from_user.username == current_user.username or post.from_user.username in friends_usernames:
            posts_from_friends.append(post)

    posts_from_friends = sorted(posts_from_friends, key = lambda x: x.written_at, reverse = True)

    context['posts'] = posts_from_friends

    return render(request, 'RFP_templates/index.html', context)

@login_required
def reserve_pitch(request):
    pitches = Pitch.objects.all()
    context = {
        'pitches' : pitches,
    }

    return render(request, 'RFP_templates/reservepitch.html', context)

@login_required
def friends(request):
    return render(request, 'RFP_templates/friends.html', {})

@login_required
def send_requests(request):
    current_user = request.user
    current_user_profile = current_user.profile

    all_users = User.objects.exclude(pk = current_user.id)

    users_not_friends = []

    for checking_user in all_users:
        friend_request_exists = FriendRequest.objects.filter(
            sender = checking_user,
            receiver = current_user
        ).exists()

        reverse_friend_request_exists = FriendRequest.objects.filter(
            sender = current_user,
            receiver = checking_user
        ).exists()

        if not friend_request_exists and not reverse_friend_request_exists and checking_user.profile not in current_user_profile.friends.all():
            users_not_friends.append(checking_user)

    return render(request, 'RFP_templates/sendrequest.html', {'not_friends': users_not_friends})

@login_required
def send_request(request, id):
    current_user = request.user
    sender = current_user
    receiver = User.objects.get(pk=id)

    friend_request = FriendRequest.objects.create(
        sender = sender,
        receiver = receiver,
    )

    receiver_profile = Profile.objects.get(user = receiver)
    receiver_profile.received_friend_requests.add(friend_request)

    current_user_profile = Profile.objects.get(user = current_user)

    all_users = User.objects.exclude(pk = current_user.id).exclude(pk = id)

    users_not_friends = []

    for checking_user in all_users:
        friend_request_exists = FriendRequest.objects.filter(
            sender = checking_user,
            receiver = current_user
        ).exists()

        reverse_friend_request_exists = FriendRequest.objects.filter(
            sender = current_user,
            receiver = checking_user
        ).exists()

        if not friend_request_exists and not reverse_friend_request_exists and checking_user.profile not in current_user_profile.friends.all():
            users_not_friends.append(checking_user)

    return render(request, 'RFP_templates/sendrequest.html', {'not_friends':users_not_friends})

@login_required
def see_friends_request(request):
    friend_requests = request.user.profile.received_friend_requests.all()

    senders = [friend_request.sender for friend_request in friend_requests]

    return render(request, 'RFP_templates/seefriendrequests.html', {'senders': senders})

@login_required
def accept_request(request, id):
    current_user = request.user
    sender = User.objects.get(pk = id)

    friend_request = FriendRequest.objects.filter(sender = sender, receiver = request.user)
    friend_request.delete()

    current_user.profile.friends.add(sender.profile)
    
    return redirect('RFP:friends')
    

@login_required
def shop(request):
    items = Item.objects.all()
    context = {
        'items' : items
    }

    return render(request, 'RFP_templates/shop.html', context)

@login_required
def detail(request, id):
    pitch = Pitch.objects.get(pk = id)

    form = ReservationForm(request.POST or None, request = request)

    if form.is_valid():
        reservation = form.save(commit = False)
        reservation.made_by = request.user
        reservation.pitch = pitch
        reservation.reservation_code = generate_random_code()
        
        reservation.save()
        reservation.participants.add(request.user)

        request.user.profile.tokens = request.user.profile.tokens + 1
        request.user.profile.save()

        messages.success(request, 'Reservation succcessfully made!')
        return redirect('RFP:reserve_pitch')

    return render(request, 'RFP_templates/detail.html', {'form':form, 'pitch':pitch})

@login_required
def add_post(request):
    post_message = request.GET.get('post')
    new_post = Post.objects.create(
        from_user = request.user,
        written_at = timezone.now(),
        message = str(post_message),
    )

    new_post.save()

    return redirect('RFP:start')

@login_required
def buy_item(request, id):
    item = Item.objects.get(pk = id)
    item_price = item.price
    
    if request.user.profile.tokens - item_price >= 0:
        request.user.profile.tokens -= item_price
        request.user.profile.save()

        BoughtItem.objects.create(
            item_name = item,
            item_code = generate_random_code(),
            bought_from = request.user
        )
        
        messages.success(request, "Item successfully bought!")
    else:
        messages.error(request, "You cannot buy the item because you do not have enough tokens!")
        return redirect('RFP:shop')

    return redirect('RFP:bought_items')

@login_required
def bought_items(request):
    bought_items = BoughtItem.objects.filter(bought_from = request.user)
    return render(request, 'RFP_templates/boughtitems.html', {'bought_items': bought_items})

@login_required
def see_reserved_pitches(request):
    reservations = Reservation.objects.all()

    current_reservations = []

    for reservation in reservations:
        if request.user in reservation.participants.all():
            current_reservations.append(reservation)
    
    return render(request, 'RFP_templates/reservations.html', {'reservations':current_reservations, 'user':request.user})

@login_required
def personal_info(request, id):
    show_user = User.objects.get(pk = id)
    return render(request, 'RFP_templates/personalinfo.html', {'shown_user' : show_user})

@login_required
def change_info(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile.age = form.cleaned_data['age']
            user_profile.city = form.cleaned_data['city']
            user_profile.position = form.cleaned_data['position']
            user_profile.image = form.cleaned_data['image']
            user_profile.save()
            return redirect('RFP:start')
    else:
        form = ProfileForm(instance = user_profile)

    return render(request, 'RFP_templates/changepersonalinfo.html', {'form': form})

@login_required
def view_friends(request):
    current_user = request.user
    friends_list = current_user.profile.friends.all()

    return render(request, 'RFP_templates/viewfriends.html', {'friends_list': friends_list})
    
@login_required
def search_items(request):
    searched_item_name = request.GET.get('input_item')
    items = Item.objects.all()
    items_names = [item.name for item in items]

    if searched_item_name in items_names:
        searched_items = Item.objects.filter(name = searched_item_name)
        items = list(searched_items)
    else:
        messages.error(request, "This item does not exist!")
        items = Item.objects.all()

    return render(request, 'RFP_templates/shop.html', {'items': items})

@login_required
def search_bought_items(request):
    searched_item_name = request.GET.get('input_item')
    items = BoughtItem.objects.filter(bought_from = request.user)
    items_names = [item.item_name.name for item in items]

    if searched_item_name in items_names:
        searched_items = items.filter(item_name__name = searched_item_name)
        items = list(searched_items)
    else:
        messages.error(request, "This item does not exist!")
        items = BoughtItem.objects.all()

    return render(request, 'RFP_templates/boughtitems.html', {'bought_items': items})

@login_required
def search_pitch(request):
    searched_pitch_name = request.GET.get('input_pitch')
    pitches = Pitch.objects.all()
    pitches_names = [pitch.name for pitch in  pitches]

    if searched_pitch_name in pitches_names:
        searched_pitches = Pitch.objects.filter(name = searched_pitch_name)
        pitches = list(searched_pitches)
    else:
        messages.error(request, "This pitch does not exist!")
        pitches = Pitch.objects.all()

    return render(request, 'RFP_templates/reservepitch.html', {'pitches' : pitches})

@login_required
def see_participants(request, id):
    reservation = Reservation.objects.get(pk = id)
    participants = reservation.participants.all()
    reservation_creator = reservation.made_by
    return render(request, 'RFP_templates/seeparticipants.html', {'users': participants, 'reservation':reservation, 'creator':reservation_creator})

@login_required
def set_code(request):
    return render(request, 'RFP_templates/setcode.html', {})

@login_required
def join_game(request):
    code = request.GET.get('input_code')
    reservations = Reservation.objects.exclude(made_by = request.user)
    reservations_codes = [reservation.reservation_code for reservation in reservations]

    if code in reservations_codes:
        current_reservation = Reservation.objects.get(reservation_code=code)
        current_reservation_creator = current_reservation.made_by
        current_reservation_creator_friends = current_reservation_creator.profile.friends.all()

        if request.user.profile in current_reservation_creator_friends:
            current_reservation.participants.add(request.user)
        else:
            messages.error(request, "You cannot join a game where the creator is not your friend!")
            return redirect('RFP:join_game')
    else:
        messages.error(request, "This game does not exist!")
        return redirect('RFP:set_code')
    
    reservations = Reservation.objects.all()

    current_reservations = []

    for reservation in reservations:
        if request.user in reservation.participants.all() or request.user == reservation.made_by:
            current_reservations.append(reservation)
    
    return render(request, 'RFP_templates/reservations.html', {'reservations':current_reservations})

@login_required
def delete_reservation(request, id):
    reservation = Reservation.objects.get(pk = id)
    request.user.profile.tokens -= 1
    request.user.profile.save()
    reservation.delete()

    return redirect('RFP:see_reserved_pitches')

@login_required
def delete_post(request, id):
    post = Post.objects.get(pk = id)
    post.delete()

    return redirect('RFP:start')

@login_required
def delete_item(request, id):
    item = BoughtItem.objects.get(pk = id)
    request.user.profile.tokens += int(item.item_name.price)
    request.user.profile.save()
    item.delete()

    return redirect('RFP:start')

@login_required
def delete_friend(request, id):
    current_user_profile = request.user.profile
    friend_to_remove = Profile.objects.get(pk = id)
    current_user_profile.friends.remove(friend_to_remove)

    return redirect('RFP:start')

@login_required
def remove_participant(request, user_id, reservation_id):
    participant = User.objects.get(pk = user_id)
    reservation = Reservation.objects.get(pk = reservation_id)

    messages.success(request, f'You have removed {participant.username}!')
    reservation.participants.remove(participant)
    reservation.save()

    participants = reservation.participants.all()
    return render(request, 'RFP_templates/seeparticipants.html', {'users': participants, 'reservation':reservation})