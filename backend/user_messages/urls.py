from django.urls import path

from .views import (
    ReceivedMessagesView,
    SentMessagesView,
    SendMessageView,
    ReadMessageView,
)

urlpatterns = [
    path('received_messages/', ReceivedMessagesView.as_view(), name='received-messages'),
    path('sent_messages/', SentMessagesView.as_view(), name='sent-messages'),
    path('send_message/', SendMessageView.as_view(), name='send-message'),
    path('messages/<int:pk>/', ReadMessageView.as_view(), name='read-message'),
]
