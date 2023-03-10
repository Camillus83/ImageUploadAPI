"""
This models.py module defines the 'Image' model and 'Thumbnail' model.

The 'Image' model represents an uploaded by user image to the application.
'Image' stores information about uploaded image like owner, filename, upload date
and URL for accesing the image.

The 'Thumbnail' model represents and Thumbnails based on 'Image' uploaded to the application.
'Thumbnail' stores informations about created Thumbnail like height expresed in px. From which
image it was created.

Both models have a custom 'save' method that automatically generate unique URL for accesing
the image or thumbnaild on current site.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model


class Image(models.Model):
    """
    The 'Image' model represents an uploaded by user image to the application.
    'Image' stores information about uploaded image like owner, filename, upload date
    and URL for accesing the image.
    """

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to="images/")
    image_url = models.URLField(default="http://127.0.0.1:8000/admin/images/image/")
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        current_site = "127.0.0.1:8000/api/v1"
        self.image_url = f"http://{current_site}/img/{uuid.uuid1()}"
        super().save(*args, **kwargs)


class Thumbnail(models.Model):
    """
    The 'Thumbnail' model represents and Thumbnails based on 'Image' uploaded to the application.
    'Thumbnail' stores informations about created Thumbnail like height expresed in px. From which
    image it was created.
    """

    height = models.PositiveIntegerField(default=200)
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="thumbnails"
    )
    thumbnail_file = models.ImageField(upload_to="thumbnails/")
    url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        current_site = "127.0.0.1:8000/api/v1"
        self.url = f"http://{current_site}/tmb/{uuid.uuid1()}"
        super().save(*args, **kwargs)
