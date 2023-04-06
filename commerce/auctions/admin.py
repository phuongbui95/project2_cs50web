from django.contrib import admin

from .models import User, Category, Listing, Bid, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username") #temporary display

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "title", "description", "listing_status", "user_type")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "listing", "price", "bid_status")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "listing", "content", "comment_status")

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
