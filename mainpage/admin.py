from django.contrib import admin
from .models import Post
from .models import Pitch
from .models import Item

# Register your models here.
admin.site.register(Post)
admin.site.register(Pitch)
admin.site.register(Item)