from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.core.exceptions import PermissionDenied

from .forms import CustomUserCreationForm
from .models import CustomUser


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
