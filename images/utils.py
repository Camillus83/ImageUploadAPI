"""
Module for utility functions for images app.
This module contains functions:
 - create_thumbnail: Create a thumbnail image from an 'Image' instance.
"""
import io
from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Thumbnail, Image


def create_thumbnail(image: Image, thumbnail_size: int) -> Thumbnail:
    """
    Create a thumbnail form an Image instance nad save it to the database.
    Generate a thumbnail image with the specified height and a width
    proportional to the aspect ratio of the original image.

    Args:
        image (Image): Image instance to create a thumbnail from.
        thumbnail_size (int): Height of the thumbnail.
    Returns:
        Thumbnail instance
    """
    thumbnail = Thumbnail()
    thumbnail.image = image
    thumbnail.height = thumbnail_size
    with PILImage.open(image.image_file) as img:
        width, heigth = img.size
        aspect_ratio = width / heigth
        new_width = int(aspect_ratio * thumbnail_size)
        img.thumbnail((new_width, thumbnail_size))
        output = io.BytesIO()
        img.convert("RGB").save(output, format="JPEG")
        output.seek(0)

        thumbnail.thumbnail_file = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{image.file_name}.jpg",
            "image/jpeg",
            output.getbuffer().nbytes,
            None,
        )

    thumbnail.save()
    return thumbnail
