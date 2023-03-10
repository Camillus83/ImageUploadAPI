from django.urls import path
from .views import UserViewSet, image_preview_view, images_view, thumbnail_preview_view

urlpatterns = [
    path("users", UserViewSet.as_view(), name="users"),
    path("img/<str:random_id>", image_preview_view, name="image_preview"),
    path("tmb/<str:random_id>", thumbnail_preview_view, name="thumbnail_preview"),
    path("images", images_view, name="upload_image"),
]
