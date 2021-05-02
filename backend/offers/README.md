# `offers` module
## Description
This module provides REST API endpoints for book offers and images for these offers.

## Endpoints
All endpoints need token authentication header: "Authorization: Token \<your-token\>"
- `/api/offers/`
    - create offer - POST method
    - read offers - GET method
    - options - OPTIONS method
- `/api/offers/<id>/` (where \<id\> is id of offer)
    - full update - PUT method
    - partial update - PATCH method
    - read offer - GET method
    - delete offer - DELETE method
    - options - OPTIONS method
- `/api/offer_images/`
    - create image for offer - POST method
    - read images for offers - GET method
    - options - OPTIONS method
- `/api/offer_images/<id>/` (where \<id\> is id of image)
    - read offer image - GET method
    - delete offer image - DELETE method
    - options - OPTIONS method
- `/api/offer_search`
    - search though offers - GET method
