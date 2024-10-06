from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('<int:pk>/', views.coffeeShop_detail, name='coffeeShop_detail'),
    path('toggle-favorite/<int:pk>/', views.toggleFavorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('search/', views.search, name='search')
    

    
]