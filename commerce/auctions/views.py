from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Category, Bid , Watchlist
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
    
    


# @login_required
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
    
@login_required(login_url='/login') #redirect to login page if user does not log-in yet
def watchlist(request):
    # Add to Watchlist
    if request.method == "POST":
        if "add_button" in request.POST:
            # scrap listing's id after hitting the "Add to Watchlist" button 
            listing_posted = Listing.objects.get(pk=request.POST["listing_id"])
            # create new Watchlist object
            if Watchlist.objects.filter(user=request.user, listing=listing_posted).exists():
                return HttpResponse('Listing already exists')
            else:
                # Create a new object in Model
                watchlist_item = Watchlist(user=request.user, listing=listing_posted)
                watchlist_item.save() #save to database's model
        elif "remove_button" in request.POST:
            item_listing_id_selected = request.POST['item_listing_id']
            # filter the listing_id in User's Watchlist model
            Watchlist.objects.filter(user=request.user, listing=item_listing_id_selected).delete()
            # check bug
            # return HttpResponse(f'Item_listing_id {item_listing_id_selected} is removed')

    # Display all items in Watchlist
    all_items = Watchlist.objects.all()[::-1]
    return render(request, 'auctions/watchlist.html', {
        'all_items': all_items
    })

@login_required(login_url='/login') #redirect to login page if user does not log-in yet
def bid(request):
    if request.method == 'POST':
        #Take posted bid_price and listing_id
        bid_price = request.POST['bid_price']
        listing_id = request.POST['listing_id']
        listing_posted = Listing.objects.get(pk=request.POST["listing_id"])
    
        #Compare newly posted bid to current bid of listing
        if int(bid_price) >= listing_posted.price:
            message = f"Your bid {bid_price} is accepted."
            # Create a new object in Bid Model
            bid_item = Bid(user=request.user, listing=listing_posted)
            # If posted Bid is existing, do not save
            if not Bid.objects.filter(user=request.user, listing=listing_posted):
                bid_item.save() #save to database's model
            else:
                message = f"Your bid {bid_price} is already on the list. Bid higher!"

            # Update price of Listing item
            Listing.objects.filter(id=listing_id).update(price=bid_price)
            # update_listing_price.save()
        else:
            message = "Bid higher! Click on 'Listing id' to bid again"

        # call out all existing bidded listings of this user
        existing_bid_listings = Bid.objects.all()[::-1]

        # response to end-user
        return render(request, "auctions/bid.html", {
            "message": message,
            "listing_posted": listing_posted,
            "existing_bid_listings": existing_bid_listings
        })
        
# @login_required
# def comment(request):
#     return render(request, "auctions/comment.html")
