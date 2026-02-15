from django.shortcuts import render
from .models import Profile, Post, Friend, Photo, Video, Chatroom

def fb_profile(request):
    profile = Profile.objects.first()
    posts = Post.objects.all().order_by('-created_at')
    # 首頁的「朋友九宮格」只需要顯示前 9 個
    friends = Friend.objects.all()[:9]
    photos = Photo.objects.all()[:9]
    
    return render(request, 'profile.html', {
        'profile': profile, 
        'posts': posts,
        'friends_amount': Friend.objects.count(),
        'friends': friends, # 傳給首頁側邊欄用
        'photos': photos,   # 傳給首頁側邊欄用
        'active_tab': 'posts' # 用來標記當前分頁
    })

def fb_friends(request):
    profile = Profile.objects.first()
    friends = Friend.objects.all()
    return render(request, 'friends.html', {
        'profile': profile,
        'friends': friends,
        'friends_amount': Friend.objects.count(),
        'active_tab': 'friends'
    })

def fb_media(request):
    profile = Profile.objects.first()
    photos = Photo.objects.all().order_by('-created_at')
    videos = Video.objects.all().order_by('-created_at') # 抓取影片
    return render(request, 'media.html', {
        'profile': profile,
        'photos': photos,
        'videos': videos,
        'friends_amount': Friend.objects.count(),
        'active_tab': 'media'
    })

def fb_about(request):
    profile = Profile.objects.first()
    return render(request, 'about.html', {
        'profile': profile,
        'friends_amount': Friend.objects.count(),
        'active_tab': 'about'
    })

def fb_messages(request, room_id=None):
    profile = Profile.objects.first() 
    rooms = Chatroom.objects.all()
    
    # 如果有傳入 room_id，就抓那一間；否則抓第一間
    if room_id:
        active_room = Chatroom.objects.get(id=room_id)
    else:
        active_room = rooms.first()
        
    messages = active_room.messages.all() if active_room else []
    
    return render(request, 'messages.html', {
        'profile': profile,
        'rooms': rooms,
        'active_room': active_room,
        'messages': messages,
        'active_tab': 'messages',
        'friends_amount': Friend.objects.count(),
    })