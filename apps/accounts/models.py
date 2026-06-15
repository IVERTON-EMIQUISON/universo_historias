from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Usuário customizado com campos extras."""
    
    READER = 'reader'
    AUTHOR = 'author'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (READER, 'Leitor'),
        (AUTHOR, 'Autor'),
        (ADMIN, 'Administrador'),
    ]
    
    email = models.EmailField(_('email'), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=READER)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_premium = models.BooleanField(default=False)
    premium_expires = models.DateTimeField(null=True, blank=True)
    reading_preferences = models.JSONField(default=dict, blank=True)
    total_points = models.IntegerField(default=0)  # Sistema de conquistas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class UserProfile(models.Model):
    """Perfil expandido do leitor."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    favorite_genres = models.ManyToManyField('stories.Category', blank=True)
    social_instagram = models.CharField(max_length=100, blank=True)
    social_twitter = models.CharField(max_length=100, blank=True)
    notifications_enabled = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    reading_font_size = models.IntegerField(default=16)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


class Achievement(models.Model):
    """Conquistas do sistema de gamificação."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # emoji ou classe CSS
    points_required = models.IntegerField(default=0)
    badge_image = models.ImageField(upload_to='badges/', null=True, blank=True)
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email