from django.contrib.auth.models import AbstractUser
from django.db import models

# Tutorial: https://docs.djangoproject.com/en/4.1/topics/db/models/
class User(AbstractUser):
    #already have fields for a username, email, password, etc., 
    # pass
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.username #present username as key instead of id
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    CATEGORY_LIST = (
        ("Electronics", "Electronics"),    
        ("Home", "Home"),
        ("Toys", "Toys"),
        ("Fashion", "Fashion"),
        ("Other", "Other"),
    )
                                       
    category_name = models.CharField(max_length=64, choices=CATEGORY_LIST, default="Other")
    # display the key as category_name but id
    def __str__(self):
        return self.category_name #display the 1st elements of each tuple

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    # null=True, blank=True => Set no default to field
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="creator") #user's id
    category = models.ForeignKey(Category, default=5, on_delete=models.CASCADE, related_name="listing_category")
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.BigIntegerField(default=10)
    image = models.ImageField(blank=True, upload_to="auctions/static/auctions/images") 
    STATUS_LIST = (
        ("Active", "Active"),    
        ("Closed", "Closed"),
    )
                                       
    status = models.CharField(max_length=64, choices=STATUS_LIST, default="Active")

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()

