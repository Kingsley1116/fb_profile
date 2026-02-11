from django.contrib import admin
from .models import Profile, Post, Friend, Photo, Video, ChatMessage, Chatroom

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title') # 在列表顯示姓名和職稱

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content_summary', 'created_at') # 顯示貼文摘要和時間
    list_filter = ('created_at',) # 右側可以按時間篩選
    search_fields = ('content',) # 讓你可以搜尋貼文內容

    def content_summary(self, obj):
        return obj.content[:30] + "..." # 只顯示前 30 個字
    content_summary.short_description = '貼文內容'


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'created_at')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'file')
    search_fields = ('title',)
    list_filter = ('created_at',)


class MessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 1

@admin.register(Chatroom)
class ChatroomAdmin(admin.ModelAdmin):
    inlines = [MessageInline]