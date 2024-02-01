from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='static/images/')
    tags = models.CharField(max_length=50)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

