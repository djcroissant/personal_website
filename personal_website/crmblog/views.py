from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.contrib import messages

from crmblog.models import Post


class HomeView(ListView):
    model = Post
    template_name = 'crmblog/home.html'

    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        return queryset.order_by('-created')[:4]     # Only need the 4 most recent posts
