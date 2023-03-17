from django.urls import path
from .views import (
    UserViewSet,
    image_preview_view,
    thumbnail_preview_view,
    image_view,
    create_expire_image_view,
    expire_image_preview_view,
    ImageUploadView,
)

urlpatterns = [
    path("users", UserViewSet.as_view(), name="users"),
    path("img/<str:random_id>", image_preview_view, name="image_preview"),
    path("tmb/<str:random_id>", thumbnail_preview_view, name="thumbnail_preview"),
    path("images", ImageUploadView.as_view(), name="images"),
    path("images/<int:id>", image_view, name="image"),
    path("images/<int:id>/exp", create_expire_image_view, name="create_expire_image"),
    path("exp/<str:random_id>", expire_image_preview_view, name="expire_image_view"),
]
