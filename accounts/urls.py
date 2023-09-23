from django.urls import path, include, re_path
from allauth.account.views import confirm_email

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    re_path(
        r"^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    path(r"rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
