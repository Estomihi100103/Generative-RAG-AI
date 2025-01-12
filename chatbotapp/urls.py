from django.urls import path
from .views import send_message, list_messages
from django.urls import include

urlpatterns = [
    path("send", send_message, name="send_message"),
    path("", list_messages, name="list_messages"),
    path("__reload__/", include("django_browser_reload.urls")),
]
