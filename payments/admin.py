from django.contrib import admin
from .models import PaymentTransaction

@admin.register(PaymentTransaction)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'transaction_id', 'created_at')
    list_filter = ('status',)