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

class Pitch(models.Model):

    def __str__(self):
        return self.name
    
    name = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length = 10)
