# views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.account.models import EmailConfirmation
from django.shortcuts import get_object_or_404


class CustomEmailConfirmView(APIView):
    def get(self, request, key):
        verify_email_url = (
            "http://localhost:8000/dj-rest-auth/registration/verify-email/"
        )

        # make a POST request to the verify-email endpoint with the key
        response = requests.post(verify_email_url, {"key": key})
        if response.status_code == 200:
            return Response(
                {"message": "Email verified successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Email verification failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
