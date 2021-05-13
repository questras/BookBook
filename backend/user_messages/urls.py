from django.urls import path

from .views import (
    ReceivedMessagesView,
    SentMessagesView,
    SendMessageView,
)

urlpatterns = [
    path('received_messages/', ReceivedMessagesView.as_view(), name='received-messages'),
    path('sent_messages/', SentMessagesView.as_view(), name='sent-messages'),
    path('send_message/', SendMessageView.as_view(), name='send-message'),
]
