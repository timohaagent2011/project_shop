from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('developer/', views.developer_dashboard, name='developer_dashboard'),
    path('developer/add/', views.add_game, name='add_game'),
        path('support/', views.support, name='support'),
]