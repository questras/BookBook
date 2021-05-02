# `token_auth` module
## Description
This module provides token-based authorization for REST API. It heavily uses [`django-rest-framework`](https://www.django-rest-framework.org/) providing authorization scheme class `token_auth.auth.TokenAuthorization` and various endpoints.

## Endpoints
- `/api/auth/acquire_token`
- `/api/auth/revoke_token`
- `/api/auth/renew_token`

To see details of given endpoint simply run application and visit e.g. [localhost:8000/api/auth/acquire_token](http://localhost:8000/api/auth/acquire_token).
