from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.

class Post(models.Model):

    def __str__(self):
        return self.from_user.username
    
    from_user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, default = 1)
    written_at = models.DateTimeField()
    message = models.CharField(max_length = 500)

class Pitch(models.Model):

    def __str__(self):
        return self.name
    
    name = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length = 10)
    image = models.CharField(max_length = 500, default = "https://static.vecteezy.com/system/resources/thumbnails/020/015/926/small_2x/football-pitch-icon-vector.jpg")

class Item(models.Model):

    def __str__(self):
        return self.name
    
    name = models.CharField(max_length = 200)
    price = models.IntegerField()
    image = models.CharField(max_length = 500, default = "https://c1.wallpaperflare.com/preview/305/482/405/music-grocer-grocery-store-sales-stand.jpg")

class BoughtItem(models.Model):
    item_name = models.ForeignKey(Item, on_delete = models.CASCADE, null =True)
    item_code = models.CharField(max_length = 10, unique = True, default = uuid.uuid4().hex[:6].upper())
    bought_from = models.ForeignKey(User, on_delete = models.CASCADE, null = True, default = 1)

    def __str__(self):
        return f"{self.item_name} - {self.item_code}"
    
class Reservation(models.Model):
    datetime = models.DateTimeField(default = timezone.localtime(timezone.now()) + timezone.timedelta(hours = 1))
    made_by = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    pitch = models.ForeignKey(Pitch, on_delete = models.CASCADE, null = True)
    reservation_code = models.CharField(max_length = 10, unique = True, default = uuid.uuid4().hex[:6].upper())
    participants = models.ManyToManyField(User, related_name = 'reservation_participants', blank = True)

    def __str__(self):
        return f"{self.pitch.name} reserved at {self.datetime} by {self.made_by.username}"