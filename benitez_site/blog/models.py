from django.core import validators
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinLengthValidator



# Create your models here.
class Tag(models.Model):
    caption = models.CharField(max_length=32)
    
    def __str__(self):
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=128)
    img_name = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, default="", blank=True, null=False, db_index=True)
    content = models.TextField(validators=[MinLengthValidator])

    # One to many relation
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")

    # Many to Many relation
    tag = models.ManyToManyField(Tag, null=True)

    def __str__(self):
        return self.title


    
    