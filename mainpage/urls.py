from . import views
from django.urls import path

app_name = 'RFP'
urlpatterns = [
    path('', views.start, name = 'start'),
    path('reservepitch/', views.reserve_pitch, name = 'reserve_pitch'),
    path('<int:id>/', views.detail, name='detail'),
    path('friends/', views.friends, name = 'friends'),
    path('friends/addfriend/', views.add_friend, name = 'add_friend'),
    path('shop/', views.shop, name = 'shop'),
    path('settings/', views.settings, name = 'settings'),
    path('addpost/', views.add_post, name='add_post'),
    path('shop/<int:id>/', views.buy_item, name='buy_item'),
    path('bought_items/', views.bought_items, name='bought_items'),
    path('reservations/', views.see_reserved_pitches, name='see_reserved_pitches'),
    path('personalinfo/<int:id>/', views.personal_info, name='personal_info'),
    path('changepersonalinfo/', views.change_info, name='change_info'),
]