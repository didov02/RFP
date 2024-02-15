from . import views
from django.urls import path

app_name = 'RFP'
urlpatterns = [
    path('', views.start, name = 'start'),
    path('reservepitch/', views.reserve_pitch, name = 'reserve_pitch'),
    path('reservepitch/<int:id>', views.make_reservation, name='make_reservation'),
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
]