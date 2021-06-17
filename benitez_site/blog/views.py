from django.shortcuts import render, get_object_or_404
from .models import Post, Author, Tag

# Create your views here.

def starting_page(request):
    # This is a single query. This makes it efficient since django does not have to fetch the whole data.
    latest_posts = Post.objects.all().order_by("-date")[:3]

    return render(request, "blog/blog-index.html", {
        'posts': latest_posts
    } )

def posts(request): 
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html", {
        'posts': all_posts
    })

def post_detail(request, slug):
    identified_post = get_object_or_404(Post,slug=slug)
    return render(request, "blog/post-detail.html", {
        'post': identified_post,
        'post_tags': identified_post.tag.all()

    })