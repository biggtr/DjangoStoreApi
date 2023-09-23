# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.account.models import EmailConfirmation
from django.shortcuts import get_object_or_404


class CustomEmailConfirmView(APIView):
    def get(self, request, key):
        # Look up the email confirmation record by key
        email_confirmation = get_object_or_404(EmailConfirmation, key=key)

        # Check if the confirmation key is expired
        if email_confirmation.key_expired:
            return Response(
                {"detail": "Email confirmation link has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark the email as verified and save the user
        email_confirmation.email_address.verified = True
        email_confirmation.email_address.save()

        return Response(
            {"detail": "Email verified successfully."}, status=status.HTTP_200_OK
        )
