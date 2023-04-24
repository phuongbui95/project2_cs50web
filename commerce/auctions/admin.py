from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment, Watchlist

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "title", "description", "price", "status","image")
    list_filter = ("user","category","status")
    search_fields = ["user__username","title","status"]

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing")
    search_fields = ["user__username","listing__title"]

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "leading_bid")
    list_filter = ("listing",)
    search_fields = ["user__username","listing__title"]
    # add a hyphen before leading_bid, this will order bids by leading_bid in descending order.
    ordering = ("listing__title","-leading_bid",) 

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "content")
    list_filter = ("user","listing")
    search_fields = ["user__username","listing__title","content"] #do not need to use __ in the same model

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)