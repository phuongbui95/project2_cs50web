from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import User, Listing, Comment, Category, Bid , Watchlist
from .forms import CreateListingForm


# # Call out categories for selection in Navigation bar
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

def listings_by_cat(request, cat_id):
    category = Category.objects.get(pk=cat_id)
    all_listings = Listing.objects.filter(Q(category=category) & Q(status="Active"))

    return render(request,"auctions/listings_by_cat.html", {
        "category_name": category,
        "all_listings": all_listings,
        "categories": categories
    })

def listing(request, listing_id):
    current_user = request.user
    listing = Listing.objects.get(pk=listing_id)

    # all comments before new comment is added
    all_comments = Comment.objects.filter(listing=listing)[::-1]
    
    if request.method == "POST":
        ##--- Close Auction
        if "close_auction" in request.POST:
            # creator
            if listing.user == current_user or listing.status=="Closed":
                message = "Auction is CLOSED"
                # Update listing_status to "closed": status = 1
                Listing.objects.filter(id=listing_id).update(status="Closed")
                
            # not creator
            else:
                # return HttpResponse("sth wrong")
                message = "Only creator can close this auction!"

            #return messages

            return render(request, "auctions/listing.html", {
                    "message": message,
                    "listing": listing,
                    "leading_bid": leading_bid,
                    "categories": categories
            })
        
        ###-- Bid section --###
        if "bid_price_submit" in request.POST:
            leading_bid = Bid.objects.filter(listing=listing).last()
            
            # Only users who signed in can comment
            if current_user.is_authenticated:
                #Take posted bid_price and listing_id
                bid_price = request.POST['bid_price']
                listing_creator = listing.user
                is_creator = current_user == listing_creator
                
                # Listing's creator cannot bid
                if is_creator:
                    message = 'Cannot bid your own listing!'
                #Compare newly posted bid to current bid of listing
                elif int(bid_price) >= listing.price:         
                    # If posted Bid of current_user is NOT existing, save
                    if not Bid.objects.filter(user=request.user, listing=listing):
                        message = "Your bid is accepted."
                        # Create a new object in Bid Model
                        Bid(user=request.user, listing=listing, leading_bid=bid_price).save()
                        # Update price of Listing item in Listing model
                        Listing.objects.filter(id=listing_id).update(price=bid_price)
                    elif Bid.objects.filter(user=request.user, listing=listing) and int(bid_price) == listing.price:
                        message = "Bid is already set."
                    else:
                        message = "Your Adjusted bid is accepted."
                        # Create a new object in Bid Model
                        Bid(user=request.user, listing=listing, leading_bid=bid_price).save()
                        # Update price of Listing item in Listing model
                        Listing.objects.filter(id=listing_id).update(price=bid_price)

                else:
                    message = "Rejected. Bid higher!"
                return render(request, "auctions/listing.html", {
                    "message": message,
                    "listing": listing,
                    "all_comments": all_comments,
                    "categories": categories,
                    "leading_bid": leading_bid,
                    "bid_price": bid_price
                
            })
            else:
                return HttpResponseRedirect(reverse("login"))
            
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
    #Call as global variable of this function
    message = 'To visit listing page, click on hyperlink of that product'

    ###--- 2. Listings to Bid --- ###
    # Add to Watchlist
    if request.method == "POST":
        if "add_button" in request.POST:
            # scrap listing's id after hitting the "Add to Watchlist" button 
            listing_posted = Listing.objects.get(pk=request.POST["listing_id"])
            listing_creator = listing_posted.user

            # create new Watchlist object
            if Watchlist.objects.filter(user=request.user, listing=listing_posted): #.exists():
                message = "Listing already exists!"
            elif current_user == listing_creator:
                message = f"You are the creator of product '{listing_posted}'"
            else:
                # Create a new object in Model
                watchlist_item = Watchlist(user=request.user, listing=listing_posted)
                watchlist_item.save() #save to database's model
        # elif "remove_button" in request.POST:
        else:
            item_listing_id_selected = request.POST['item_listing_id']
            # filter the listing_id in User's Watchlist model
            Watchlist.objects.filter(user=request.user, listing=item_listing_id_selected).delete()
            removed_listing = Listing.objects.get(pk=item_listing_id_selected)
            message = f"You removed product '{removed_listing}' from your watchlist"


    # Display all items in Watchlist
    bid_listings = Watchlist.objects.all()[::-1]
    return render(request, 'auctions/watchlist.html', {
        'my_listings': my_listings,
        'bid_listings': bid_listings,
        "categories": categories,
        "message": message
    })
