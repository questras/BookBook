# `users` module
## Description
This module provides REST API endpoints and logic for user-related functionalities.

## Endpoints
- `/api/auth/register`
- `/api/auth/change_password/`
    - PUT method
    - Needs authentication
- `/api/auth/profile/<id>/` (where \<id\> is id of a user)
    - GET method
    - Needs authentication
- `/api/auth/my_profile/`
    - Current user's profile
    - GET method
    - Needs authentication
