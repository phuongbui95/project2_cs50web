from django.contrib.auth.models import AbstractUser
from django.db import models

# Tutorial: https://docs.djangoproject.com/en/4.1/topics/db/models/
class User(AbstractUser):
    #already have fields for a username, email, password, etc., 
    # def __str__(self):
    #     return f"{self.id}: {self.username} ({self.email})"
    pass
    

class Category(models.Model):
    CATEGORY_LIST = models.TextChoices('CATEGORY_LIST', 
                                       'Electronics Toys Home Fashion')
    name = models.CharField(blank=True, choices=CATEGORY_LIST.choices, max_length=64)
    # def __str__(self):
    #     return f"{self.id}: {self.name}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    LISTING_STATUS = (
        (0, 'active'),
        (1, 'closed'),
    )
    listing_status = models.IntegerField(choices=LISTING_STATUS)

    USER_TYPE = (
        (0, 'none'),
        (1, 'creator'),
        (2, 'bidder'),
    )
    user_type = models.IntegerField(choices=USER_TYPE)

    image = models.ImageField(blank=True, upload_to="auctions/static/auctions/media") 
    # def __str__(self):
    #     return f"{self.id}: {self.title} /n {self.description}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.BigIntegerField()
    BID_STATUS = (
        (0, 'live'),
        (1, 'chosen'),
        (2, 'archived'),
    )
    bid_status = models.IntegerField(choices=BID_STATUS)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()
    COMMENT_STATUS = (
        (0, 'live'),
        (1, 'deleted'),
    )
    comment_status = models.IntegerField(choices=COMMENT_STATUS)

