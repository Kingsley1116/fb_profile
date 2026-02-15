from django.db import models
from django.contrib.auth.models import User

# 個人資料（FB 的 Header 部分）
class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='profile/')
    cover_photo = models.ImageField(upload_to='profile/')

    # 工作與學歷
    company = models.CharField(max_length=100, default="大清朝廷")
    school = models.CharField(max_length=100, default="嘉慶進士")
    # 居住地
    current_city = models.CharField(max_length=100, default="福建省侯官縣")
    hometown = models.CharField(max_length=100, default="福建福州")
    # 基本資料
    gender = models.CharField(max_length=10, default="男")
    birthday = models.CharField(max_length=50, default="1785年8月30日")
    # 感情狀況
    relationship_status = models.CharField(max_length=50, default="已婚")

    def __str__(self):
        return self.name


# 貼文（FB 的 Timeline 部分）
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="發帖時間")
    likes_count = models.IntegerField(default=0)
    # comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.content[:20]}..."
    
    @property
    def comments_count(self):
        return self.comments.count()
    

# 留言
class Comment(models.Model):
    # 這則留言屬於哪篇貼文
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments_made', verbose_name="留言者")
    content = models.TextField(verbose_name="留言內容")
    created_at = models.DateTimeField(verbose_name="留言時間")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.name} 的留言"


# 朋友
class Friend(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='friends/', default='friends/default_avatar.png', blank=True, null=True)
    description = models.CharField(max_length=100, default="朝廷同僚")
    
    def __str__(self):
        return self.name


# 相片
class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"相片: {self.caption}"
    

class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="影片標題", blank=True)
    file = models.FileField(upload_to='videos/', verbose_name="影片檔案")
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True, verbose_name="影片封面")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上傳時間")

    class Meta:
        verbose_name = "影片"
        verbose_name_plural = "影片"

    def __str__(self):
        return self.title if self.title else f"影片 {self.id}"
    

class Chatroom(models.Model):
    participants = models.ManyToManyField('Profile', related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 顯示聊天室中的參與者姓名
        names = ", ".join([p.name for p in self.participants.all()])
        return f"聊天室: {names}"


class ChatMessage(models.Model):
    room = models.ForeignKey(Chatroom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('Profile', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # 讓訊息按時間順序排列

    def __str__(self):
        return f"{self.sender.name}: {self.content[:20]}"
    

class LifeEvent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='life_events')
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=20) # 例如: 1839年
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "人生大事"