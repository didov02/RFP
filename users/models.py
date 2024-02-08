from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='profile_pictures')
    age = models.IntegerField(default=15)
    city = models.CharField(max_length = 200, default='Unknown')
    position = models.CharField(max_length = 200, default='Unknown')

    def __str__(self):
        return self.user.username
    