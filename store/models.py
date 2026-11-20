from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    developer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='developed_games',
        verbose_name='Разработчик'
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Обложка')
    is_available = models.BooleanField(default=True, verbose_name='Доступна')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-created_at']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменён'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма')

    def __str__(self):
        return f'Заказ #{self.id} — {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.game.title} в заказе #{self.order.id}'

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решено'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', verbose_name='Пользователь')
    subject = models.CharField(max_length=200, verbose_name='Тема обращения')
    message = models.TextField(verbose_name='Описание проблемы')
    admin_reply = models.TextField(blank=True, verbose_name='Ответ поддержки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'#{self.id} — {self.subject} ({self.user.username})'

    class Meta:
        verbose_name = 'Обращение в поддержку'
        verbose_name_plural = 'Обращения в поддержку'
        ordering = ['-created_at']
