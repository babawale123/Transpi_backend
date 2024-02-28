from django.urls import path
from .views import SignupView,LoginView


urlpatterns = [
    path('', SignupView.as_view()),
    path('login/', LoginView.as_view()),
]