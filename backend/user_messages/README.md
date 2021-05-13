# `user_messages` module

## Description

This module provides REST API endpoints for messages between users.

## Endpoints

All endpoints need token authentication header: "Authorization: Token \<your-token\>"

- `/api/received_messages/`
    - Messages received by current user
    - GET method
- `/api/sent_messages/`
    - Messages sent by current user
    - GET method
- `/api/send_message/`
    - Send a message to another user.
    - POST method
- `/api/messages/<id>/` (where \<id\> is id of message)
    - Get a specific message.
    - GET method