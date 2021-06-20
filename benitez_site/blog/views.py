from typing import List
from django import views
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic import FormView, CreateView

from .models import Post, Author, Tag

# Create your views here.

# Using TemplateView class
# class StartingPageView(TemplateView):
#     # Render Template
#     template_name = "blog/blog-index.html"
#    
#     # Send list of last 3 posts to template
#     def get_context_data(self, **kwargs):
#         latest_posts = Post.objects.all().order_by("-date")[:3]
#         # This is an empty dictionary.
#         context =  super().get_context_data(**kwargs)
#         # Transfer context to template.
#         context["posts"] = latest_posts
#         return context

# Using ListView class
class StartingPageView(ListView):
    template_name = "blog/blog-index.html"
    model = Post
    ordering = ["-date"]
    # By default, you can use object_list
    context_object_name = "posts"

    # To get only latest 3
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# Using TemplateView class
# class PostsView(TemplateView):
#     template_name = "blog/all-posts.html"
#
#     def get_context_data(self, **kwargs):
#         all_posts = Post.objects.all().order_by("-date")
#         context = super().get_context_data(**kwargs)
#         context['posts'] = all_posts
#         return context

# Using ListView class
# Alternative to previous class
class PostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


# Using DetailView class
class PostDetailView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tag.all()
        return context


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post,slug=slug)
#     return render(request, "blog/post-detail.html", {
#         'post': identified_post,
#         'post_tags': identified_post.tag.all()
#     })