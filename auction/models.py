# auction/models.py
import json
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from datetime import datetime
from django.conf import settings

class Auction(models.Model):
    image_url = models.URLField(max_length=500, blank=True, null=True)
    date_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    avg_piece_weight = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_step = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # New field for bid increment
    end_date = models.DateTimeField(blank=True, null=True)
    closed = models.BooleanField(default=False)  # New field to mark auctions as open/closed
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True) 


    def __str__(self):
        return f"{self.date_type} - {self.category} (Price: {self.price})"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']  # Newest bids first

    def __str__(self):
        return f"Bid by {self.user.username} for {self.price}"
