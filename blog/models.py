from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    pub_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=140, null=False, blank=False)
    answer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

