from django.shortcuts import render
from django.utils.timezone import now
from django.utils import timezone
import json
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Auction, Bid
from django.conf import settings
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required

ALLOWED_USERS = ['mostafa@test.com', 'user1@example.com', 'user2@example.com']

def auction_list(request):
    # Fetch all auctions from the database
    auctions = Auction.objects.filter(is_active=True)
    # Get the selected status values from the request
    selected_status = request.GET.getlist('status')

    # Apply filtering based on the selected status
    if 'open' in selected_status:
        auctions = auctions.filter(closed=False, is_active=True)
    
    if 'closed' in selected_status:
        auctions = auctions.filter(closed=True, winner=None, is_active=True)
    
    if 'won' in selected_status:
        auctions = auctions.filter(winner=True, is_active=True)

    # Render the template with auctions data
    response = render(request, 'auction/auction_list.html', {'auctions': auctions})
    
    # Add cache-control headers to prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@login_required
def place_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    if auction.closed:
        return JsonResponse({"error": "Auction is closed or has ended."}, status=400)

    # Create a new bid
    new_price = auction.price + auction.bid_step
    bid = Bid.objects.create(
        auction=auction,
        user=request.user,
        price=new_price
    )

    # Update the auction price
    auction.price = new_price
    auction.save()

    # Redirect to the auction detail page to show the updated bids
    return redirect('auction_detail', auction_id=auction.id)


def current_price(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    bids = Bid.objects.filter(auction=auction).order_by('-date')
    
    # Return the current price and the latest bids
    bids_list = [{"user": bid.user.username, "price": bid.price, "date": bid.date.strftime("%Y-%m-%d %H:%M:%S")} for bid in bids]
    
    return JsonResponse({
        'new_price': auction.price,
        'bids': bids_list
    })


@staff_member_required
def close_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    auction.closed = True
    auction.save()
    return redirect('auction_list')  # Redirect to auction list or wherever you want

@staff_member_required
def open_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    auction.closed = False
    auction.save()
    return redirect('auction_list')  # Redirect to auction list or wherever you want

def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    bids = auction.bids.all()  # Fetch all bids for the auction, sorted by newest first
    return render(request, 'auction/auction_detail.html', {'auction': auction, 'bids': bids})

@login_required
def mark_as_won(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    
    if not request.user.is_staff:
        return redirect('auction_detail', auction_id=auction_id)

    highest_bid = auction.bids.order_by('-price').first()

    if highest_bid:
        auction.winner = highest_bid.user
        auction.closed = True  # Mark auction as closed when won
        auction.save()

    return redirect('auction_detail', auction_id=auction.id)