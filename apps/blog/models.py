from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from apps.accounts.models import User


class BlogPost(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    
    STATUS_CHOICES = [
        (DRAFT, 'Rascunho'),
        (PUBLISHED, 'Publicado'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    tags = models.ManyToManyField('stories.Tag', blank=True)
    views = models.IntegerField(default=0)
    reading_time = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        words = len(self.content.split())
        self.reading_time = max(1, words // 200)
        super().save(*args, **kwargs)