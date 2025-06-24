# Django Backend Authentication API

## Overview

The Django backend now supports JWT-based authentication that matches the frontend expectations. The backend is running on `http://localhost:8000`.

## Environment Setup

Make sure your frontend `.env.local` file contains:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Available Endpoints

### Authentication Endpoints

#### 1. **POST /auth/register**
Register a new user.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com", 
  "password": "securepassword123",
  "password2": "securepassword123",
  "role": "guest", // "guest" or "landlord"
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890" // optional
}
```

**Response:**
```json
{
  "access_token": "jwt_access_token_here",
  "refresh_token": "jwt_refresh_token_here", 
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "guest",
    "name": "John Doe",
    "isActive": true,
    "joinedAt": "2025-06-24T02:05:36.123Z"
  },
  "expires_in": 3600
}
```

#### 2. **POST /auth/login**
Login with email and password.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:** Same as register response.

#### 3. **POST /auth/refresh**
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "jwt_refresh_token_here"
}
```

**Response:**
```json
{
  "access_token": "new_jwt_access_token_here",
  "expires_in": 3600
}
```

#### 4. **GET /auth/me**
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe", 
  "email": "john@example.com",
  "role": "guest",
  "name": "John Doe",
  "isActive": true,
  "joinedAt": "2025-06-24T02:05:36.123Z"
}
```

#### 5. **POST /auth/logout**
Logout and blacklist refresh token (requires authentication).

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Request Body:**
```json
{
  "refresh_token": "jwt_refresh_token_here"
}
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

## Test Users

For testing, the following users are available:

| Role | Email | Password | Username |
|------|-------|----------|----------|
| Guest | guest@test.com | testpass123 | testguest |
| Landlord | landlord@test.com | testpass123 | testlandlord |
| Admin | admin@test.com | testpass123 | testadmin |

## User Roles

- **guest**: Regular users who can browse and book
- **landlord**: Users who can create and manage listings  
- **admin**: Full access to all features

## Authentication Flow

1. User registers or logs in → receives JWT tokens
2. Frontend stores tokens securely
3. Include `Authorization: Bearer <access_token>` header in protected requests
4. Refresh tokens automatically when they expire
5. Logout blacklists the refresh token

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (Next.js frontend)
- `http://127.0.0.1:3000`

## Token Lifetimes

- **Access Token**: 1 hour
- **Refresh Token**: 7 days (with rotation)

## Error Responses

All authentication errors return appropriate HTTP status codes:

- `400`: Bad Request (missing fields, validation errors)
- `401`: Unauthorized (invalid credentials, expired tokens)
- `403`: Forbidden (insufficient permissions)

Example error response:
```json
{
  "error": "Invalid credentials"
}
```

## Integration Notes

The Django backend now fully supports the authentication system expected by the Next.js frontend. The JWT tokens are compatible with the frontend's auth context and token management system.

Make sure both servers are running:
- Frontend: `npm run dev` on port 3000
- Backend: `python manage.py runserver` on port 8000
