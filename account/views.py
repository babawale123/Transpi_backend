
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer,User


class SignupView(APIView):
    def post(self, request):
        data = UserSerializer(data=request.data)
        
        if data.is_valid():
            user = data.save()
            user.set_password(request.data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)

            # Send email verification
            #send_email_verification(user)

            return Response({'access': str(refresh.access_token), 'data': data.data})
        
        return Response(data.errors)
    
class LoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])

        if not user.check_password(request.data['password']):
            return Response({'invalid password'})
        
        data = UserSerializer(instance=user)
        token = RefreshToken.for_user(user)
        return Response({'access': str(token.access_token), 'data': data.data})



# class SignupView(APIView):
#     def post(self,request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             user = User.objects.get(email=request.data['email'])
#             user.set_password(request.data['password'])
#             user.save()
#             token = Token.objects.create(user=user)
#             return Response({'token': token.key, 'user': serializer.data})
#         return Response(serializer.errors)





