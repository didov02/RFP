from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Post(models.Model):

    def __str__(self):
        return self.from_user
    
    from_user = models.CharField(max_length = 200, default='unknown')
    written_at = models.DateTimeField()
    message = models.CharField(max_length = 500)
    image = models.ImageField()

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
    image = models.CharField(max_length = 500, default="https://c1.wallpaperflare.com/preview/305/482/405/music-grocer-grocery-store-sales-stand.jpg")

class BoughtItem(models.Model):
    item_name = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_code = models.CharField(max_length=10, unique=True, default=uuid.uuid4().hex[:6].upper())
    bought_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)

    def __str__(self):
        return f"{self.item_name} - {self.item_code}"