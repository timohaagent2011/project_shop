from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'Покупатель'),
        ('developer', 'Разработчик'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name='Роль')

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    @property
    def is_developer(self):
        return self.role == 'developer'

# Автоматически создаем профиль для любого пользователя (включая старых и админов)
@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()
