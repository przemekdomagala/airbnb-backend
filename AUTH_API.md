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

## Admin API Endpoints

The following endpoints are available only to users with the `admin` role. All admin endpoints require authentication with an admin user's JWT token.

### User Management

#### 1. **GET /api/admin/users/**
List all users with filtering and search capabilities.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Query Parameters:**
- `search`: Search by username, email, first_name, or last_name
- `ordering`: Order by date_joined, username, or email (prefix with `-` for descending)

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/admin/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "phone_number": "+1234567890",
      "role": "guest",
      "is_active": true,
      "is_staff": false,
      "is_superuser": false,
      "date_joined": "2025-06-24T02:05:36.123Z",
      "last_login": "2025-06-24T10:30:00.000Z"
    }
  ]
}
```

#### 2. **POST /api/admin/users/**
Create a new user.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Request Body:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepassword123",
  "password2": "securepassword123",
  "first_name": "New",
  "last_name": "User",
  "phone_number": "+1234567890",
  "role": "guest",
  "is_active": true,
  "is_staff": false,
  "is_superuser": false
}
```

**Response:**
```json
{
  "id": 51,
  "username": "newuser",
  "email": "newuser@example.com",
  "first_name": "New",
  "last_name": "User",
  "phone_number": "+1234567890",
  "role": "guest",
  "is_active": true,
  "is_staff": false,
  "is_superuser": false,
  "date_joined": "2025-06-24T12:00:00.000Z",
  "last_login": null
}
```

#### 3. **GET /api/admin/users/{id}/**
Get detailed information about a specific user.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Response:** Same as single user object in list response.

#### 4. **PUT /api/admin/users/{id}/**
Update a user's information.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Request Body:** (all fields optional except id)
```json
{
  "email": "updated@example.com",
  "first_name": "Updated",
  "role": "landlord",
  "is_active": false,
  "password": "newpassword123"
}
```

#### 5. **PATCH /api/admin/users/{id}/**
Partially update a user's information.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Request Body:** (any subset of user fields)
```json
{
  "role": "admin"
}
```

#### 6. **DELETE /api/admin/users/{id}/**
Delete a user account.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Response:**
```
204 No Content
```

### Admin Actions

#### 7. **POST /api/admin/users/{id}/activate/**
Activate a user account.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Response:**
```json
{
  "status": "User activated"
}
```

#### 8. **POST /api/admin/users/{id}/deactivate/**
Deactivate a user account.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Response:**
```json
{
  "status": "User deactivated"
}
```

#### 9. **POST /api/admin/users/{id}/change_role/**
Change a user's role.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Request Body:**
```json
{
  "role": "landlord"
}
```

**Response:**
```json
{
  "status": "User role changed to landlord",
  "user": {
    "id": 1,
    "username": "johndoe",
    "role": "landlord",
    // ... other user fields
  }
}
```

#### 10. **GET /api/admin/users/stats/**
Get user statistics.

**Headers:**
```
Authorization: Bearer jwt_access_token_here
```

**Response:**
```json
{
  "total_users": 50,
  "active_users": 45,
  "inactive_users": 5,
  "role_distribution": {
    "guest": 40,
    "landlord": 8,
    "admin": 2
  }
}
```

### Admin API Access Control

- Only users with `role: "admin"` can access these endpoints
- Returns `403 Forbidden` for non-admin users
- Returns `401 Unauthorized` for unauthenticated requests

### Example Usage

```javascript
// Get user statistics
const response = await fetch('http://localhost:8000/api/admin/users/stats/', {
  headers: {
    'Authorization': `Bearer ${adminAccessToken}`,
    'Content-Type': 'application/json'
  }
});

// Change user role
await fetch(`http://localhost:8000/api/admin/users/${userId}/change_role/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${adminAccessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ role: 'landlord' })
});
```

## Error Responses

All admin API errors return appropriate HTTP status codes:

- `400`: Bad Request (validation errors, invalid data)
- `401`: Unauthorized (invalid or missing token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (user not found for specific endpoints)
- `405`: Method Not Allowed (invalid HTTP method for endpoint)

Example error response:
```json
{
  "error": "User not found"
}
```
