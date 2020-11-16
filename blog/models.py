from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.CharField(max_length=255, null=False, blank=False)
    body = models.TextField(max_length=255, null=False, blank=False)
    pub_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.title
