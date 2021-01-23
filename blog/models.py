from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core import mail
from taggit.managers import TaggableManager

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

class post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='author', related_query_name='author_name')
    thumbnail = models.ImageField(default='avatar-2.jpg')
    title = models.CharField(max_length=100)
    #slug = models.SlugField(max_length=50)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

class Comments(models.Model):
    posts = models.ForeignKey(post, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    name = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return '{} says: {}'.format(self.name, self.body)
