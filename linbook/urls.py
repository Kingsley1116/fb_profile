from django.urls import path
from . import views

app_name = 'linbook'

urlpatterns = [
    path('', views.fb_profile, name='profile'),
    path('friends/', views.fb_friends, name='friends'),
    path('media/', views.fb_media, name='media'),
    path('about/', views.fb_about, name='about'),
    path('messages/', views.fb_messages, name='messages'),
    path('messages/<int:room_id>/', views.fb_messages, name='messages_with_id'),
]