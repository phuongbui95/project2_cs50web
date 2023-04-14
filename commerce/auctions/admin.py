from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment, Watchlist

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "title", "description", "bid_price", "image")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "listing", "price")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "listing", "content")

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
