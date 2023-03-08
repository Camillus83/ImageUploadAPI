"""
Module with forms for user creation and user change for the 'CustomUser' model.

'CustomUserCreationForm' class is a form for creating new users with the fields listed in 'fields'
parameter.
It extends the built-in 'UserCreationForm'.

'CustomUserChangeForm' class is a form for changing existing users with the fields listed in the
'fields' parameter.
It extends the built-in 'UserChangeForm'.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """
    'CustomUserCreationForm' class is a form for creating new users with the fields listed in
    the 'fields' parameter.
    It extends the built-in 'UserCreationForm'.
    """

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "is_active",
            "role",
        )


class CustomUserChangeForm(UserChangeForm):
    """
    'CustomUserChangeForm' class is a form for changing existing users with the fields listed in
    the 'fields' parameter.
    It extends the built-in 'UserChangeForm'.
    """

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "is_active",
            "role",
        )
