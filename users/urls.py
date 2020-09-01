from django.urls import path

from .views import SignupView, ProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
]
