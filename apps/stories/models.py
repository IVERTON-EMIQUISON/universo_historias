from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from apps.accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#E91E8C')  # hex
    
    CHOICES = [
        ('romance', 'Romance'),
        ('fantasy', 'Fantasia'),
        ('drama', 'Drama'),
        ('suspense', 'Suspense'),
        ('fanfic', 'Fanfic'),
        ('lgbtq', 'LGBTQ+'),
        ('adventure', 'Aventura'),
    ]
    
    class Meta:
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Story(models.Model):
    STATUS_ONGOING = 'ongoing'
    STATUS_COMPLETED = 'completed'
    STATUS_PAUSED = 'paused'
    STATUS_DRAFT = 'draft'
    
    STATUS_CHOICES = [
        (STATUS_ONGOING, 'Em andamento'),
        (STATUS_COMPLETED, 'Concluída'),
        (STATUS_PAUSED, 'Pausada'),
        (STATUS_DRAFT, 'Rascunho'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    cover_image = models.ImageField(upload_to='covers/stories/')
    synopsis = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    has_sensitive_content = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='pt-BR')
    total_views = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'História'
        verbose_name_plural = 'Histórias'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def chapter_count(self):
        return self.chapters.filter(is_published=True).count()


class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300)
    content = models.TextField()
    chapter_number = models.IntegerField()
    is_published = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    word_count = models.IntegerField(default=0)
    reading_time = models.IntegerField(default=0)  # em minutos
    author_note = models.TextField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['chapter_number']
        unique_together = ('story', 'chapter_number')
    
    def __str__(self):
        return f"{self.story.title} - Cap. {self.chapter_number}: {self.title}"
    
    def save(self, *args, **kwargs):
        # Calcula contagem de palavras e tempo de leitura
        words = len(self.content.split())
        self.word_count = words
        self.reading_time = max(1, words // 200)  # ~200 palavras/min
        if not self.slug:
            self.slug = slugify(f"capitulo-{self.chapter_number}-{self.title}")
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


class Comment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comentário de {self.author.username}"


class Rating(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('story', 'user')


class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # % lido
    read_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'chapter')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'story')


class ChapterLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'chapter')


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    url = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']