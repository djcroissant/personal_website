from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from crmblog.models import Post
from .forms import ContactForm


class EmailFormListView(FormMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(EmailFormListView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Thanks for reaching out. Your message was sent successfully.')
        return super(EmailFormListView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class WebHomeView(EmailFormListView):
    model = Post
    template_name = 'crmblog/web_home.html'
    form_class = ContactForm
    success_url = reverse_lazy('crmblog:webhome')

    def get_queryset(self):
        queryset = super(WebHomeView, self).get_queryset()
        queryset = queryset.filter(tags__name__in=["web development"])
        return queryset.order_by('-created')[:4]     # Only need the 4 most recent posts


class WebPostListView(EmailFormListView):
    model = Post
    template_name = 'crmblog/web_archive.html'
    form_class = ContactForm
    success_url = reverse_lazy('crmblog:archive')

    def get_queryset(self):
        queryset = super(WebPostListView, self).get_queryset()
        queryset = queryset.filter(tags__name__in=["web development"])
        return queryset.order_by('-posted_date')


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'crmblog/post_detail.html'
    form_class = ContactForm
    success_url = reverse_lazy('crmblog:webhome')

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Thanks for reaching out. Your message was sent successfully.')
        return super(PostDetailView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('crmblog:post_detail', kwargs = {'slug': self.kwargs['slug']})


class ProjectListView(EmailFormListView):
    model = Post
    template_name = 'crmblog/projects.html'
    form_class = ContactForm
    success_url = reverse_lazy('crmblog:projects')

    def get_queryset(self):
        queryset = super(WebPostListView, self).get_queryset()
        queryset = queryset.filter(tags__name__in=["feature project"])
        return queryset.order_by('-posted_date')
