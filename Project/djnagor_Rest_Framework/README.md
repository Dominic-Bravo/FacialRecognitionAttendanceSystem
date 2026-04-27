# Django REST Framework Auth + CRUD API

Complete DRF project with:
- JWT login/signup
- Role-based permission (`admin`, `manager`, `user`)
- Email verification
- Forgot/reset password
- OAuth login via Google, Facebook, GitHub (provider access token -> API JWT)
- User-owned CRUD with relational models (`Category` -> `Item`)
- Swagger and ReDoc API documentation
- Celery background email sending

## Setup

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Run migrations:
   - `python manage.py migrate`
3. Start server:
   - `python manage.py runserver`
4. Start Celery worker (in another terminal):
   - `celery -A config worker --pool=solo --loglevel=info`

Email backend is console by default, so verification and reset links appear in terminal output.
For async email, make sure Redis is running on `127.0.0.1:6379` or update `CELERY_BROKER_URL`.

## Core Endpoints

### Auth
- `POST /api/auth/signup/`
- `POST /api/auth/login/`
- `POST /api/auth/token/refresh/`
- `POST /api/auth/verify-email/`
- `POST /api/auth/forgot-password/`
- `POST /api/auth/reset-password/`
- `POST /api/auth/oauth-login/`
- `GET /api/auth/me/`

### CRUD
- `GET/POST /api/categories/`
- `GET/PUT/PATCH/DELETE /api/categories/{id}/`
- `GET/POST /api/items/`
- `GET/PUT/PATCH/DELETE /api/items/{id}/`
- `GET /api/admin/items/` (admin/manager only)

### API Documentation
- `GET /api/schema/` (OpenAPI schema)
- `GET /api/docs/swagger/` (Swagger UI)
- `GET /api/docs/redoc/` (ReDoc)

## Payload Examples

### Signup
```json
{
  "email": "user@example.com",
  "username": "user1",
  "password": "StrongPass123!",
  "confirm_password": "StrongPass123!",
  "role": "user"
}
```

### Login
```json
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

### OAuth Login
```json
{
  "provider": "google",
  "access_token": "provider-access-token"
}
```

### Create Category
```json
{
  "name": "Personal",
  "description": "My private category"
}
```

### Create Item
```json
{
  "category": 1,
  "name": "My Item",
  "description": "Only owner can access this",
  "price": "9.99",
  "is_active": true
}
```

## Notes

- Ownership is enforced in querysets and object permissions; users can only access their own categories/items.
- Role-based example endpoint is `/api/admin/items/`.
- For production, replace console email backend and secure environment variables.
