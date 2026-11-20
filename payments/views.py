import uuid
import random
import string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Order
from .models import PaymentTransaction


def generate_game_key():
    parts = [''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3)]
    return 'GMS-' + '-'.join(parts)


@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'paid':
        return redirect('payment_success', order_id=order.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'card')
        
        transaction, created = PaymentTransaction.objects.get_or_create(
            order=order,
            defaults={'amount': order.total, 'status': 'pending'}
        )
        transaction.status = 'succeeded'
        transaction.transaction_id = str(uuid.uuid4())
        transaction.save()

        order.status = 'paid'
        order.save()

        method_names = {'card': 'Банковская карта', 'sbp': 'СБП', 'yoomoney': 'ЮMoney'}
        user_email = request.user.email or 'указанную при регистрации почту'
        games_titles = ', '.join(item.game.title for item in order.items.all())

        messages.success(
            request,
            f'Оплата через «{method_names.get(payment_method, "Карта")}» прошла успешно! '
            f'Электронный чек по заказу #{order.id} (игры: {games_titles}) и ключи активации отправлены на вашу почту {user_email}.'
        )
        
        return redirect('payment_success', order_id=order.id)

    return render(request, 'store/checkout.html', {'order': order})


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items_with_keys = [
        {'item': item, 'key': generate_game_key()}
        for item in order.items.all()
    ]
    return render(request, 'payments/payment_success.html', {
        'order': order,
        'items_with_keys': items_with_keys,
    })
