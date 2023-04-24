from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings_by_cat/<int:cat_id>", views.listings_by_cat, name="listings_by_cat"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    
    #require to login
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
]

# Add directory for Media uploading
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)