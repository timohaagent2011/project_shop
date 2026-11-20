from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Game, Order, OrderItem, SupportTicket
from .forms import GameForm, SupportTicketForm


def home(request):
    games = Game.objects.filter(is_available=True)[:6]
    return render(request, 'home.html', {'games': games})


def game_list(request):
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'new')
    games = Game.objects.filter(is_available=True)
    if query:
        games = games.filter(title__icontains=query)
    if sort == 'price_asc':
        games = games.order_by('price')
    elif sort == 'price_desc':
        games = games.order_by('-price')
    else:
        games = games.order_by('-created_at')
    return render(request, 'store/game_list.html', {'games': games, 'query': query, 'sort': sort})


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk, is_available=True)
    return render(request, 'store/game_detail.html', {'game': game})


@login_required
def cart_add(request, pk):
    game = get_object_or_404(Game, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(game.id)] = cart.get(str(game.id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'«{game.title}» добавлена в корзину.')
    return redirect('cart_view')


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for game_id, qty in cart.items():
        game = Game.objects.filter(pk=game_id).first()
        if game:
            item_total = game.price * qty
            items.append({'game': game, 'qty': qty, 'total': item_total})
            total += item_total
    return render(request, 'store/cart.html', {'items': items, 'total': total})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Корзина пуста.')
        return redirect('game_list')

    order = Order.objects.create(user=request.user, status='pending')
    total = 0
    for game_id, qty in cart.items():
        game = Game.objects.filter(pk=game_id).first()
        if game:
            for _ in range(qty):
                OrderItem.objects.create(order=order, game=game, price=game.price)
                total += game.price
    order.total = total
    order.save()

    request.session['cart'] = {}
    return redirect('payment_page', order_id=order.id)


@login_required
def developer_dashboard(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_developer:
        messages.error(request, 'Доступ разрешён только разработчикам.')
        return redirect('home')
    my_games = Game.objects.filter(developer=request.user)
    return render(request, 'store/developer_dashboard.html', {'games': my_games})


@login_required
def add_game(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_developer:
        messages.error(request, 'Доступ разрешён только разработчикам.')
        return redirect('home')
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user
            game.save()
            messages.success(request, 'Игра успешно опубликована!')
            return redirect('developer_dashboard')
    else:
        form = GameForm()
    return render(request, 'store/add_game.html', {'form': form})


def support(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Чтобы отправить обращение, войдите в аккаунт.')
            return redirect('login')
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(
                request,
                f'Ваше обращение #{ticket.id} принято! Ответ появится здесь и будет продублирован на {request.user.email or "вашу почту"}.'
            )
            return redirect('support')
    else:
        form = SupportTicketForm()

    tickets = SupportTicket.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'store/support.html', {'form': form, 'tickets': tickets})
