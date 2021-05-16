# `offer_requests` module
## Description
This module provides REST API endpoints for book requests and state changing for these requests.

## Endpoints
All endpoints need token authentication header: "Authorization: Token \<your-token\>"
- `/api/requests/`
    - create requests- POST method
    - read request - GET method
    - options - OPTIONS method
- `/api/requests/<id>/` (where \<id\> is id of request)
    - full update - PUT method
    - partial update - PATCH method
    - read offer - GET method
    - delete offer - DELETE method
    - options - OPTIONS method
- `/api/requests/<id>/accept/` (where \<id\> is id of request)
    - lent book tot this requester - POST method
    - options - OPTIONS method
- `/api/requests/<id>/reject/` (where \<id\> is id of request)
    - reject this request - POST method
    - options - OPTIONS method
- `/api/requests/<id>/finish/` (where \<id\> is id of request)
    - book has been returned - POST method
    - options - OPTIONS method
- `/api/offers/<id>/requests/` (where \<id\> is id of offer)
    - read offer's requests - GET method
