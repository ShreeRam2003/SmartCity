from django.urls import path,re_path
from django.conf.urls.static import static
from . import views
from django.conf import settings


urlpatterns = [
    path("", views.landingpage, name="landingpage"),
    path("saferoute", views.search, name="index"),
    path("saferoute/search", views.search, name="search"),
    path("saferoute/routing", views.routing, name="routing"),
    path("saferoute/police", views.police, name="police"),
    path("saferoute/cammera", views.cammera, name="cammera"),
    path("saferoute/contact", views.contact, name="contact"),
    path("saferoute/register", views.register, name="register"),
    path("saferoute/login", views.login_view, name="login"),
    path("saferoute/logout", views.logout_view, name="logout"),
    path("saferoute/getLocation",views.get_location, name= "getLocation")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)