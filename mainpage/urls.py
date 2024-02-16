from . import views
from django.urls import path

app_name = 'RFP'
urlpatterns = [
    path('', views.start, name = 'start'),
    path('reservepitch/', views.reserve_pitch, name = 'reserve_pitch'),
    path('<int:id>/', views.detail, name='detail'),
    path('friends/', views.friends, name = 'friends'),
    path('shop/', views.shop, name = 'shop'),
    path('settings/', views.settings, name = 'settings'),
    path('addpost/', views.add_post, name='add_post'),
    path('shop/<int:id>/', views.buy_item, name='buy_item'),
    path('bought_items/', views.bought_items, name='bought_items'),
    path('reservations/', views.see_reserved_pitches, name='see_reserved_pitches'),
    path('personalinfo/<int:id>/', views.personal_info, name='personal_info'),
    path('changepersonalinfo/', views.change_info, name='change_info'),
    path('friends/addfriends/', views.send_requests, name='send_requests'),
    path('friends/viewfriends/', views.view_friends, name='view_friends'),
    path('friends/acceptrequest/<int:id>', views.accept_request, name='accept_request'),
    path('friends/sendrequests/<int:id>', views.send_request, name='send_request'),
    path('friends/seefriendrequests/', views.see_friends_request, name='see_friends_request'),
    path('searchitem/', views.search_items, name='search_items'),
    path('searchpitch/', views.search_pitch, name='search_pitch'),
    path('seeparticipants/<int:id>/', views.see_participants, name='see_participants'),
    path('setcode/', views.set_code, name='set_code'),
    path('joingame/', views.join_game, name='join_game'),
    path('deletereservation/<int:id>/', views.delete_reservation, name='delete_reservation'),
    path('searchboughtitem/', views.search_bought_items, name='search_bought_items'),
    path('deletepost/<int:id>', views.delete_post, name='delete_post'),
    path('deleteitem/<int:id>', views.delete_item, name='delete_item'),
]