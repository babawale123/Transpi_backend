from django.urls import path
from .views import SignupView,LoginView,EmailVerificationView


urlpatterns = [
    path('', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify/<str:token>/', EmailVerificationView.as_view(), name='email-verification'),
]