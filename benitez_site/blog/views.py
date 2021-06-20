from typing import List
from django import views
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic import FormView, CreateView
from django.urls import reverse

from .models import Post, Author, Tag
from .forms import Comment, CommentForm

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


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post,slug=slug)
#     return render(request, "blog/post-detail.html", {
#         'post': identified_post,
#         'post_tags': identified_post.tag.all()
#     })


# Using DetailView class
# class PostDetailView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post
#
#     def get_context_data(self, **kwargs):
#         # Empty dict.
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tag.all()
#         context["comment_form"] = CommentForm()
#         return context

# Using generic View class to handle comments on posts.
class PostDetailView(View):
    def is_stored_post(self, request, post_id):
        # To remove the Read later button, we need to check if the current post id is
        # in our session.
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later


    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
        

    def post(self, request, slug):
        # Store submitted data.
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            # Since form is based on a model form, I can use .save().
            # Since model excludes 1 field which is not filled by user, it must be filled by the backend.
            # First store the user data without submitting comment to DB, then assign a post to the comment, THEN submit.
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("posts-detail-page", args=[slug]))
        
        context = {
            "post": post,
            "post_tags": post.tag.all(), 
            "comment_form": comment_form,
            "comments": post.comments.all.order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }

        return render(request, "blog/post-detail.html", context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            # id__in is a MODIFIER (check documentation for more)
            # Returns all the posts that match the ids in the session.
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        
        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        # Validate if there is a stored post id in the session
        if stored_posts is None:
            stored_posts = []

        # If there isnt, generate the post id and store it in the session.
        post_id = int(request.POST["post_id"])
        
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        
        # Need this to update session's key.
        request.session["stored_posts"] = stored_posts

        post_slug = request.POST["post_slug"]
        print(post_slug)
        return HttpResponseRedirect(f"/posts/{post_slug}")

