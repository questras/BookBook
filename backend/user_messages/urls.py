from django.urls import path

from .views import (
    ReceivedMessagesView,
    SentMessagesView,
)

urlpatterns = [
    path('received_messages/', ReceivedMessagesView.as_view(), name='received-messages'),
    path('sent_messages/', SentMessagesView.as_view(), name='sent-messages'),
]
