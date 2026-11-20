from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'description', 'price', 'cover', 'is_available')

from .models import SupportTicket

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ('subject', 'message')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Например: Не пришёл ключ активации'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Опишите вашу проблему подробнее...'}),
        }
