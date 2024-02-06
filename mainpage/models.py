from django.db import models

# Create your models here.
class User(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length = 200)
    email = models.EmailField(unique = True)
    age = models.IntegerField()
    city = models.CharField(max_length = 200)
    position = models.CharField(max_length = 200)

class Post(models.Model):

    def __str__(self):
        return self.from_user
    
    from_user = models.CharField(max_length = 200)
    written_at = models.TimeField()
    message = models.CharField(max_length = 500)
    image = models.CharField(max_length = 500, default = "https://static.vecteezy.com/system/resources/previews/007/319/933/original/black-avatar-person-icons-user-profile-icon-vector.jpg")

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