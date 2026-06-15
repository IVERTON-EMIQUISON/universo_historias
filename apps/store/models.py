from django.db import models

# Create your models here.
from django.db import models
from apps.accounts.models import User


class Product(models.Model):
    EBOOK = 'ebook'
    PHYSICAL = 'physical'
    
    TYPE_CHOICES = [
        (EBOOK, 'E-book'),
        (PHYSICAL, 'Livro Físico'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='products/')
    product_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)  # -1 = ilimitado (ebooks)
    isbn = models.CharField(max_length=20, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    file = models.FileField(upload_to='ebooks/', null=True, blank=True)  # para ebooks
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.price


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    @property
    def total(self):
        return self.product.current_price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField()
    max_uses = models.IntegerField(default=100)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendente'),
        (STATUS_PAID, 'Pago'),
        (STATUS_SHIPPED, 'Enviado'),
        (STATUS_DELIVERED, 'Entregue'),
        (STATUS_CANCELLED, 'Cancelado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)