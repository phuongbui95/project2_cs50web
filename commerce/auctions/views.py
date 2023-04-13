from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Category, Bid, Watchlist
from .forms import CreateListingForm

# get the data from Listing model
def index(request):
    all_listing = Listing.objects.all()[::-1]
    return render(request, "auctions/index.html", {
        "all_listing": all_listing
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def category(request):
    category = Category.objects.all()
    return render(request,"auctions/category.html", {
        "category": category
    })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing is not None:
        return render(request, "auctions/listing.html", {
            "listing": listing
        })
    else:
        raise Http404("Listing does not exist")

@login_required
def create(request):
    if request.POST:
        form = CreateListingForm(request.POST, request.FILES)
        # print(request.FILES)
        # check if form data is valid (server-side)
        if form.is_valid():
            form.save()
            # Redirect user to active listing
            return HttpResponseRedirect(reverse("index"))   
        else:
            # If the form is invalid, re-render the page with existing information.
            render(request,"auctions/create.html", {
                'form': form
            })

    return render(request,"auctions/create.html", {
        'form': CreateListingForm()
    })
    
# @login_required
def watchlist(request):
    # create a url_list of particular user
    id_list=[]
    if request.method == 'POST':
        # Save url to database
        listing_id = request.POST.get('listing_id')
        id_list.append(listing_id)

    user = User.objects.get(pk=user.id)
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist,
    })

# @login_required
# def bid(request):
#     if request.method == "POST":
#         listing_id = request.POST
#         listing = Listing.objects.get(pk=listing_id)
#         user = User.objects.get(pk=user_id)
#         bid = Bid.objects.get(pk=bid_id)
#         return render(request, "auctions/bid.html", {
#             "listing": listing,
#             "user": user,
#             "bid": bid
#         })
#     else:
#         return render(request, "auctions/bid.htm", {
#             "message": "Please input an existing listing id."
#         })
    

# @login_required
# def comment(request):
#     return render(request, "auctions/comment.html")
