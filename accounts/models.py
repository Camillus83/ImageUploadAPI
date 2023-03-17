"""
This models.py module defines the custom user model and role model.

The 'Role' model represents a user role in the application. Each role has a name, thumbnail size and
flags indicating if user is allower to generate original image url or url with expiration.

The 'CustomUser' model extends Django's built in 'AbstractUser' model and adds a field 'role' which
is a foreign key to Role model, by that users can be assigned to different permission levels in the
app. If the role is not specified, default role is Basic.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    """
    Representing a user role in app.
    name - role name
    thumbnail_size - just thumbnail size :)
    allow_original - permission to generate url with original photo.
    allow_expiring - permission to generate expiring url.
    """

    name = models.CharField(max_length=20, unique=True)
    thumbnail_size = models.PositiveIntegerField(default=200)
    allow_original = models.BooleanField(default=False)
    allow_expiring = models.BooleanField(default=False)

    def __str__(self):
        """Returning name of a role."""
        return str(self.name)


class CustomUser(AbstractUser):
    """
    The 'CustomUser' model extends Django's built in 'AbstractUser' model and adds a field 'role'
    which is a foreign key to Role model, by that users can be assigned to different permission
    levels in the app.
    If the role is not specified, default role is Basic.
    """

    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
