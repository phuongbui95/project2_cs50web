from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import User, Listing, Comment, Category, Bid , Watchlist
from .forms import CreateListingForm

# This variable is used for all pages
# Call out categories for selection in Navigation bar
categories = Category.objects.all()

# get the data from Listing model
def index(request):
    # Only display listings which status = "Active"
    all_listings = Listing.objects.filter(status="Active")[::-1]
    return render(request, "auctions/index.html", {
        "all_listings": all_listings,
        "categories": categories
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
        return render(request, "auctions/login.html", {"categories": categories})


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
                "message": "Passwords must match.",
                "categories": categories
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "categories": categories
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {"categories": categories})

# not used
def category(request):
    categories = Category.objects.all()
    return render(request,"auctions/category.html", {
        "categories": categories
    })

def listings_by_cat(request, cat_id):
    category = Category.objects.get(pk=cat_id)
    all_listings = Listing.objects.filter(Q(category=category) & Q(status="Active"))

    return render(request,"auctions/listings_by_cat.html", {
        "category_name": category,
        "all_listings": all_listings,
        "categories": categories
    })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # this_category = listing.category
    # products = Listing.objects.filter(Q(category=this_category) & Q(status="Active")).order_by('?')[:5]

    # all comments before new comment is added
    all_comments = Comment.objects.filter(listing=listing)[::-1]
    
    if request.method == "POST":
        current_user = request.user
        # Close Auction
        if "close_auction" in request.POST:
            # creator
            if listing.user == current_user or listing.status=="Closed":
                message = "Auction is NOW closed"
                # Update listing_status to "closed": status = 1
                Listing.objects.filter(id=listing_id).update(status="Closed")
                
            # not creator
            else:
                message = "Only creator can close this auction!"
            
            # find bid winner
            # winning_bid = Bid.objects.get(listing=listing)
            winning_bid = Bid.objects.filter(listing=listing).first()

            #return messages

            return render(request, "auctions/listing.html", {
                    "message": message,
                    "listing": listing,
                    "bid": winning_bid,
                    "categories": categories,
                    # "products": products
            })
        
        ###-- Comment section --###
        if "comment" in request.POST:
            # Only users who signed in can comment
            if current_user.is_authenticated:
                # If comment submitted, add user (current_user) and content to Comment Model
                content = request.POST["comment"]
                # Create a new object in Model
                comment = Comment(user=current_user, listing=listing, content=content)
                comment.save() #save to database's model

                # Call the newly updated all_comments
                all_comments = Comment.objects.filter(listing=listing)[::-1]
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "all_comments": all_comments,
                    "categories": categories,
                    # "products": products
            })
            else:
                return HttpResponseRedirect(reverse("login"))

    else:
        ######--------####
        if listing is not None:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "all_comments": all_comments,
                "categories": categories,
                # "products": products
            })
        else:
            raise Http404("Listing does not exist")
    
@login_required(login_url='/login') #redirect to login page if user does not log-in yet
def create(request):
    if request.POST:
        form = CreateListingForm(request.POST, request.FILES)
        
        # check if form data is valid (server-side)
        print(form.errors)
        if form.is_valid():
            
            # call out listing's data from form
            listing = form.save(commit=False)
            # add user to listing's data
            listing.user = request.user
            listing.save()
            # Redirect user to active listing
            return HttpResponseRedirect(reverse("index"))   
        else:
            # If the form is invalid, re-render the page with existing information.
            return HttpResponse("Sth wrong!")
            render(request,"auctions/create.html", {
                'form': form,
                "categories": categories
            })

    return render(request,"auctions/create.html", {
        'form': CreateListingForm(),
        "categories": categories
    })
    
@login_required(login_url='/login') #redirect to login page if user does not log-in yet
def watchlist(request):
    ###--- 1. Your created listings --- ###
    current_user = request.user
    my_listings = Listing.objects.filter(user=current_user)

    ###--- 2. Listings to Bid --- ###
    # Add to Watchlist
    if request.method == "POST":
        if "add_button" in request.POST:
            # scrap listing's id after hitting the "Add to Watchlist" button 
            listing_posted = Listing.objects.get(pk=request.POST["listing_id"])
            listing_creator = listing_posted.user

            # create new Watchlist object
            if Watchlist.objects.filter(user=request.user, listing=listing_posted): #.exists():
                return HttpResponse('Listing already exists')
            elif current_user == listing_creator:
                return HttpResponse('You are the creator of this listing!')
            else:
                # Create a new object in Model
                watchlist_item = Watchlist(user=request.user, listing=listing_posted)
                watchlist_item.save() #save to database's model
        # elif "remove_button" in request.POST:
        else:
            item_listing_id_selected = request.POST['item_listing_id']
            # filter the listing_id in User's Watchlist model
            Watchlist.objects.filter(user=request.user, listing=item_listing_id_selected).delete()


    # Display all items in Watchlist
    bid_listings = Watchlist.objects.all()[::-1]
    return render(request, 'auctions/watchlist.html', {
        'my_listings': my_listings,
        'bid_listings': bid_listings,
        "categories": categories
    })

@login_required(login_url='/login') #redirect to login page if user does not log-in yet
def bid(request):
    current_user = request.user
    if request.method == 'POST':
        #Take posted bid_price and listing_id
        bid_price = request.POST['bid_price']
        listing_id = request.POST['listing_id']
        listing_posted = Listing.objects.get(pk=listing_id)
        listing_creator = listing_posted.user

        # Listing's creator cannot bid
        if current_user == listing_creator:
            message = 'Cannot bid your own listing!'
        #Compare newly posted bid to current bid of listing
        elif int(bid_price) >= listing_posted.price:         
        # If posted Bid is existing, do not save
            if not Bid.objects.filter(user=request.user, listing=listing_posted):
                message = f"Bid {bid_price} is accepted."
                # Create a new object in Bid Model
                bid_item = Bid(user=request.user, listing=listing_posted)
                bid_item.save() #save to database's model
            elif Bid.objects.filter(user=request.user, listing=listing_posted) and int(bid_price) == listing_posted.price:
                message = f"Bid is already set."
            else:
                message = f"Changed your bid to {bid_price}."

            # Update price of Listing item
            Listing.objects.filter(id=listing_id).update(price=bid_price)
            # update_listing_price.save()
        else:
            message = "Rejected. Bid higher!"

        # call out all existing bidded listings of this user
        existing_bid_listings = Bid.objects.all()[::-1]

        # response to end-user
        return render(request, "auctions/bid.html", {
            "message": message,
            "listing_posted": listing_posted,
            "existing_bid_listings": existing_bid_listings,
            "categories": categories
        })
     
