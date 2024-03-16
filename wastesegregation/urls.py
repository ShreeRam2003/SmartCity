from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Maps the root URL to the index view
    path('ws', views.websocket_endpoint),  # Maps the /ws URL to the websocket_endpoint view
]
