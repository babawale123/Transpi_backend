
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken  
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer,User

from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework import status
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupView(APIView):
    def post(self, request):
        data = UserSerializer(data=request.data)
        
        if data.is_valid():
            user = data.save()
            user.set_password(request.data['password'])
            user.save()

            # Send email verification
            send_email_verification(user)

            return Response({'message': 'User registered successfully. Check your email for verification.'})
        
        return Response(data.errors)

def send_email_verification(user):
    # Generate a unique token for email verification
    access_token = RefreshToken.for_user(user).access_token

    # Build the verification URL
    verification_url = f' http://127.0.0.1:8000/api/auth/verify/{access_token}/'

    # Send the email
    subject = 'Email Verification'
    message = f'Please click the following link to verify your email: {verification_url}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    send_mail(subject, message, from_email, [to_email])

# Use a signal to send email verification after the user is saved
@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        send_email_verification(instance)
    
class LoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])

        if not user.check_password(request.data['password']):
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_verified:
            return Response({'error': 'User not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        data = UserSerializer(instance=user).data
        token = RefreshToken.for_user(user)
        return Response({'access': str(token.access_token), 'data': data})


        



class EmailVerificationView(APIView):
    def get(self, request, token):
        try:
            # Decode the token to get the user ID
            decoded_token = AccessToken(token)
            user_id = decoded_token.payload['user_id']

            # Retrieve the user instance
            user = get_object_or_404(User, id=user_id)

            # Mark the user as verified (customize as needed)
            user.is_verified = True
            user.save()

            return Response({'message': 'Email verification successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

