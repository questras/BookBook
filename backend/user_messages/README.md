# `user_messages` module
## Description
This module provides REST API endpoints for messages between users.

## Endpoints
All endpoints need token authentication header: "Authorization: Token \<your-token\>"
- `/api/received_messages/`
    - Messages received by current user
- `/api/sent_messages/`
    - Messages sent by current user
