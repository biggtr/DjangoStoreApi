from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "membership",
            "phone",
        ]
        error_messages = {
            "email": {
                "unique": "This Email is Already Taken. Please choose a different one.",
            },
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "membership",
            "phone",
        ]

        error_messages = {
            "email": {
                "unique": "This Email is Already Taken. Please choose a different one.",
            },
        }
