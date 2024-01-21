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
]