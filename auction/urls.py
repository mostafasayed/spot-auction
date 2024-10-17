# auction/urls.py (in the auction app)
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.auction_list, name='auction_list'),
    path('auction/<int:auction_id>/bid/', views.place_bid, name='place_bid'),
    path('auction/<int:auction_id>/current_price/', views.current_price, name='current_price'),
    path('auction/<int:auction_id>/close/', views.close_auction, name='close_auction'),
    path('auction/<int:auction_id>/open/', views.open_auction, name='open_auction'),
    path('auction/<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('auction/<int:auction_id>/mark_as_won/', views.mark_as_won, name='mark_as_won'),


]