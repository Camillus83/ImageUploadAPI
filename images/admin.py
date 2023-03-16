from django.contrib import admin
from .models import Image, Thumbnail, ExpiringImage

# Register your models here.

admin.site.register(Image)
admin.site.register(Thumbnail)
admin.site.register(ExpiringImage)
