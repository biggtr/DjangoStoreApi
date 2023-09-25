from django.urls import path, include, re_path
from allauth.account.views import confirm_email
from .views import CustomEmailConfirmView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    re_path(
        r"^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        CustomEmailConfirmView.as_view(),
        name="account_confirm_email",
    ),
    path(r"registration/", include("dj_rest_auth.registration.urls")),
]
