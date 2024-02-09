from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='profile_pictures')
    age = models.IntegerField(default=15)
    city = models.CharField(max_length = 200, default='Unknown')
    position = models.CharField(max_length = 200, default='Unknown')
    tokens = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    received_friend_requests = models.ManyToManyField('FriendRequest', related_name='receiver_friend_requests', blank=True)

    def __str__(self):
        return self.user.username
    

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')

    def __str__(self):
        return f'{self.sender} -> {self.receiver}'
    