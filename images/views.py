import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    PermissionDenied,
)
from django.http import HttpResponse, HttpResponseGone, Http404

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from accounts.models import CustomUser, Role
from .models import Image, Thumbnail, ExpiringImage
from .serializers import UserSerializer, ImageSerializer, ThumbnailSerializer
from .utils import create_thumbnail
from datetime import datetime, timedelta


def image_preview_view(request, random_id):
    """
    A view that retrieves an Image object by its URL and returns the image data
    as a HTTP response.

    Args:
        request (HttpRequest): A Django HTTP request object.
        random_id (str): A random identifier that corresponds to the Image object's URL.
    """
    try:
        image = Image.objects.get(
            image_url=f"http://127.0.0.1:8000/api/v1/img/{random_id}"
        )
    except Image.DoesNotExist:
        raise Http404("Image does not exist.")
    with image.image_file.open() as img:
        image_data = img.read()
    return HttpResponse(image_data, content_type="image/jpeg")


def thumbnail_preview_view(request, random_id):
    """
    A view that retrieves an Thumbnail object by its URL and returns the image data
    as a HTTP response.

    Args:
        request (HttpRequest): A Django HTTP request object.
        random_id (str): A random identifier that corresponds to the Thumbnail object's URL.
    """
    try:
        image = Thumbnail.objects.get(
            url=f"http://127.0.0.1:8000/api/v1/tmb/{random_id}"
        )
    except Thumbnail.DoesNotExist:
        raise Http404("Thumbnail does not exist.")
    with image.thumbnail_file.open() as img:
        image_data = img.read()
    return HttpResponse(image_data, content_type="image/jpeg")


@login_required
@api_view(
    [
        "POST",
    ]
)
def create_expire_image_view(request, id):
    """
    A view that creates an expiring URL for an Image object.
    Args:
        request (Request): Django HTTP request object.
        id (int): ID of the image object.
    Returns:
        DRF response object that contains the expiring URL.

    """
    try:
        # Get Image
        image = Image.objects.get(pk=id)
        # Check if requestes user is owner of the image.
        if image.owner != request.user:
            raise PermissionDenied("You are not authorized to view this image.")
        # Check if request user have permission to create expiring urls.
        if not request.user.role.allow_expiring:
            raise PermissionDenied("You are not allowed to create expiring images.")
    except ObjectDoesNotExist:
        # If Image with given ID doesn't exists.
        raise ValidationError("Image with that ID doesn't exists")
    except MultipleObjectsReturned:
        raise ValidationError(
            "There are more than one image with that ID. Contact administrator."
        )

    # Check if time to expire is between 300 and 30000. Like in requirements
    time_to_expire = request.data.get("time_to_expire")
    if int(time_to_expire) < 300 or int(time_to_expire) > 30000:
        raise ValidationError("Time to expire must be between 300 and 30000 seconds.")
    # Create new object
    expire_url = ExpiringImage()
    expire_url.image = image
    expire_url.expire_time = datetime.now() + timedelta(seconds=int(time_to_expire))
    expire_url.save()
    response_data = {"expiring_url": expire_url.url}
    return Response(response_data)


@api_view(["GET"])
def expire_image_preview_view(request, random_id):
    """
    Retrieve an expiring image preview given its random ID.

    This view receives a GET request with a `random_id` parameter that identifies
    the expiring image to retrieve. If the image exists and its expiration time
    has not passed yet, it returns an HTTP response with the image data and the
    "image/jpeg" content type. If the image link has expired, it deletes the
    expiring image object and returns an HTTP response with status code 410 Gone.

    Parameters:
    - `request`: The HTTP request object.
    - `random_id` (str): The random ID that identifies the expiring image.
      Returns:
    - `HttpResponse` with the image data and content type, or status code 410 Gone.
    """
    try:
        image = ExpiringImage.objects.get(
            url=f"http://127.0.0.1:8000/api/v1/exp/{random_id}"
        )
    except ObjectDoesNotExist:
        return HttpResponseGone("The image doesn't exist or the link has expired.")

    if datetime.now() > image.expire_time:
        image.delete()
        return HttpResponseGone("The image link has expired.")

    with image.image.image_file.open() as img:
        image_data = img.read()

    return HttpResponse(image_data, content_type="image/jpeg")


@login_required
@api_view(["GET"])
def image_view(request, id):
    """
    View to retrieve image details.

    Args:
        request (Request): Django HTTP request object.
        id (int): The ID of the image.
    """
    try:
        image = Image.objects.get(pk=id)
        if image.owner != request.user:
            raise PermissionDenied("You are not authorized to view this image.")
    except ObjectDoesNotExist:
        raise ValidationError("Image with that ID doesn't exists")
    except MultipleObjectsReturned:
        raise ValidationError(
            "There are more than one image with that ID. Contact administrator."
        )

    thumbnail_data = {}
    thumbnails = image.thumbnails.all()
    for thumbnail in thumbnails:
        thumbnail_data[f"{thumbnail.height}px_url"] = thumbnail.url
    original_url = image.image_url if request.user.role.allow_original else None
    response_data = {
        "image_id": image.pk,
        "filename": image.file_name,
        "original_url": original_url,
        "thumbnails": thumbnail_data,
    }
    return Response(response_data)


class ImageUploadView(generics.CreateAPIView, generics.ListAPIView):
    """
    API endpoint that allows authenticated users to upload images and
    view their uploaded images and associated thumbnails.

    A POST request with a valid JPEG or PNG image file to this endpoint
    will create a new Image object associated with the authenticated user,
    store the uploaded image file, create and store its thumbnails, and
    return the URLs of the generated thumbnails and, if allowed by the user's
    role, the URL of the original image.

    A GET request to this endpoint will return a JSON object containing
    information about all images uploaded by the authenticated user,
    including their IDs, filenames, original URLs (if allowed), and URLs
    of their thumbnails.

    Only authenticated users with a valid role are authorized to access this view.
    """

    queryset = Image.objects.none()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        image_file = request.FILES.get("image_file")

        user = request.user
        if user.role is None:
            raise ValidationError("User should have an role.")

        filename, extension = os.path.splitext(image_file.name)
        new_filename = f"{filename}_{user.username}{extension}"

        if Image.objects.filter(file_name=image_file.name).exists():
            raise ValidationError("Image with the same name field already exists.")

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

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role is None:
            raise ValidationError("User should have an role.")
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
                "image_id": image.pk,
                "filename": image.file_name,
                "original_url": original_url,
                "thumbnails": thumbnail_data,
            }
        return Response(response_data)


class UserViewSet(generics.ListAPIView):
    """
    A view that returns a list of all users in the system.

    Users must be authenticated in order to access this view.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
