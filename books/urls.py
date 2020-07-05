from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from books.views import HomepageView


urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about')
]
