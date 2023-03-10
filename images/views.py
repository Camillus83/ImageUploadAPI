import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from accounts.models import CustomUser, Role
from .models import Image, Thumbnail
from .serializers import UserSerializer, ImageSerializer, ThumbnailSerializer
from .utils import create_thumbnail


def image_preview_view(request, random_id):

    image = Image.objects.get(image_url=f"http://127.0.0.1:8000/api/v1/img/{random_id}")
    print(image)
    with image.image_file.open() as img:
        image_data = img.read()
    return HttpResponse(image_data, content_type="image/jpeg")


def thumbnail_preview_view(request, random_id):

    image = Thumbnail.objects.get(url=f"http://127.0.0.1:8000/api/v1/tmb/{random_id}")
    with image.thumbnail_file.open() as img:
        image_data = img.read()
    return HttpResponse(image_data, content_type="image/jpeg")


@login_required
@api_view(["POST", "GET"])
@parser_classes([MultiPartParser, FormParser])
def images_view(request):
    if request.method == "POST":
        image_file = request.data.get("image")
        user = request.user

        filename, extension = os.path.splitext(image_file.name)
        new_filename = f"{filename}_{user.username}{extension}"

        if Image.objects.filter(file_name=image_file.name).exists():
            raise ValidationError("Image with the same field already exists.")

        if not (
            image_file.content_type == "image/jpeg"
            or image_file.content_type == "image/png"
        ):
            raise ValidationError("Only JPEG and PNG image formats are supported.")

        image = Image(image_file=image_file, owner=user, file_name=new_filename)
        image.save()

        thumbnail_sizes = {
            "Basic": [Role.objects.get(name="Basic").thumbnail_size],
            "Premium": [
                Role.objects.get(name="Basic").thumbnail_size,
                Role.objects.get(name="Premium").thumbnail_size,
            ],
            "Enterprise": [
                Role.objects.get(name="Basic").thumbnail_size,
                Role.objects.get(name="Premium").thumbnail_size,
            ],
        }

        if user.role.name not in ["Basic", "Premium", "Enterprise"]:
            thumbnail_sizes[user.role.name] = [user.role.thumbnail_size]

        thumbnail_data = {}
        for size in thumbnail_sizes[user.role.name]:
            thumbnail = create_thumbnail(image, size)
            thumbnail_data[f"{size}px_thumbnail"] = ThumbnailSerializer(thumbnail).data

        if user.role.name == "Enterprise" or user.role.allow_original:
            thumbnail_data["original_image"] = ImageSerializer(image).data

        return Response(thumbnail_data)
    elif request.method == "GET":
        user = request.user
        images = Image.objects.filter(owner=user)
        response_data = {}
        for i, image in enumerate(images, start=1):

            thumbnail_data = {}
            thumbnails = image.thumbnails.all()
            for thumbnail in thumbnails:
                thumbnail_data[f"{thumbnail.height}px_url"] = thumbnail.url
            if user.role.allow_original:
                original_url = image.image_url
            else:
                original_url = None
            response_data[f"image{i}"] = {
                "filename": image.file_name,
                "original_url": original_url,
                "thumbnails": thumbnail_data,
            }
        return Response(response_data)


class UserViewSet(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
