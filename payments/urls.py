from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:order_id>/', views.payment_page, name='payment_page'),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
]