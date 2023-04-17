from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    
    #require to login
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.bid, name="bid"),
    # path("result", views.result, name="result"),
    # path("comment", views.comment, name="comment"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)