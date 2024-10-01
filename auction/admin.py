from django.contrib import admin
from .models import Auction

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('date_type', 'category', 'price', 'bid_step', 'quantity', 'closed')
    list_editable = ('bid_step', 'closed')