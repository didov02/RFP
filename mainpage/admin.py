from django.contrib import admin
from .models import Post
from .models import Pitch
from .models import Item
from .models import BoughtItem
from .models import Reservation

# Register your models here.
admin.site.register(Post)
admin.site.register(Pitch)
admin.site.register(Item)
admin.site.register(BoughtItem)
admin.site.register(Reservation)