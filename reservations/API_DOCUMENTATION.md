# Reservations API Documentation

## Overview
The reservations module handles the complete booking flow for the DreamBook platform, supporting a 3-step booking process as implemented in the frontend.

## API Endpoints

### Base URL: `/api/reservations/`

## Reservation Management

### List/Create Reservations
- **GET** `/api/reservations/` - List user's reservations
- **POST** `/api/reservations/` - Create a new reservation

#### Query Parameters (GET)
- `status` - Filter by status: `pending`, `confirmed`, `cancelled`, `completed`
- `payment_status` - Filter by payment status: `pending`, `paid`, `refunded`

#### Create Reservation Payload (POST)
```json
{
  "listing_id": "uuid-string",
  "check_in": "2024-07-15",
  "check_out": "2024-07-17",
  "guests_adults": 2,
  "guests_children": 0,
  "guest_first_name": "John",
  "guest_last_name": "Doe",
  "guest_email": "john@example.com",
  "guest_phone": "+1234567890",
  "special_requests": "Late check-in",
  "payment_method": "card"
}
```

### Individual Reservation
- **GET** `/api/reservations/{id}/` - Get reservation details
- **PUT** `/api/reservations/{id}/` - Update reservation
- **DELETE** `/api/reservations/{id}/` - Delete reservation

### Reservation by Confirmation Number
- **GET** `/api/reservations/confirmation/{confirmation_number}/` - Get reservation by confirmation number

### Reservation Actions
- **POST** `/api/reservations/{id}/cancel/` - Cancel a reservation
- **POST** `/api/reservations/{id}/confirm/` - Confirm and process payment

#### Confirm Payment Payload
```json
{
  "payment": {
    "card": {
      "last_four": "1234",
      "brand": "Visa"
    }
  }
}
```

## 3-Step Booking Process

### Step 1: Guest Information Validation
- **POST** `/api/reservations/booking/step-1/`

```json
{
  "listing_id": "uuid-string",
  "check_in": "2024-07-15",
  "check_out": "2024-07-17",
  "guests_adults": 2,
  "guests_children": 0,
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "specialRequests": "Late check-in"
}
```

### Step 2: Payment Information Validation
- **POST** `/api/reservations/booking/step-2/`

```json
{
  "payment_method": "card",
  "card_details": {
    "number": "4242424242424242",
    "expiry": "12/25",
    "cvv": "123",
    "name": "John Doe"
  }
}
```

### Step 3: Final Confirmation
- **POST** `/api/reservations/booking/step-3/`

```json
{
  "listing_id": "uuid-string",
  "check_in": "2024-07-15",
  "check_out": "2024-07-17",
  "guests_adults": 2,
  "guests_children": 0,
  "guest_first_name": "John",
  "guest_last_name": "Doe",
  "guest_email": "john@example.com",
  "guest_phone": "+1234567890",
  "special_requests": "Late check-in",
  "payment_method": "card"
}
```

## Availability Management

### Check Availability
- **POST** `/api/reservations/availability/check/`

```json
{
  "listing_id": "uuid-string",
  "check_in": "2024-07-15",
  "check_out": "2024-07-17"
}
```

**Response:**
```json
{
  "available": true,
  "listing_id": "uuid-string",
  "check_in": "2024-07-15",
  "check_out": "2024-07-17",
  "conflicts": 0
}
```

### Availability Blocks (Landlord)
- **GET** `/api/reservations/availability/blocks/` - List availability blocks
- **POST** `/api/reservations/availability/blocks/` - Create availability block

## History and Reports

### User Reservation History
- **GET** `/api/reservations/history/`

#### Query Parameters
- `status` - Filter by status
- `year` - Filter by year

### Landlord Reservations
- **GET** `/api/reservations/landlord/`

#### Query Parameters
- `status` - Filter by status
- `listing_id` - Filter by specific listing

## Data Models

### Reservation Object
```json
{
  "id": "uuid-string",
  "confirmation_number": "DB12345678",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "listing": {
    "id": "uuid-string",
    "title": "Beautiful Apartment",
    "location": "New York, NY",
    "price_per_night": "199.00"
  },
  "check_in": "2024-07-15",
  "check_out": "2024-07-17",
  "guests_adults": 2,
  "guests_children": 0,
  "total_nights": 2,
  "guest_first_name": "John",
  "guest_last_name": "Doe",
  "guest_name": "John Doe",
  "guest_email": "john@example.com",
  "guest_phone": "+1234567890",
  "special_requests": "Late check-in",
  "price_per_night": "199.00",
  "subtotal": "398.00",
  "taxes_and_fees": "59.70",
  "total_amount": "457.70",
  "status": "confirmed",
  "payment_status": "paid",
  "payment_method": "card",
  "created_at": "2024-07-14T10:30:00Z",
  "updated_at": "2024-07-14T10:30:00Z",
  "payment": {
    "id": 1,
    "payment_provider": "stripe",
    "card_last_four": "1234",
    "card_brand": "Visa",
    "amount_paid": "457.70",
    "currency": "PLN",
    "paid_at": "2024-07-14T10:30:00Z"
  }
}
```

## Frontend Integration

### Booking Flow Integration

The frontend's 3-step booking process should integrate as follows:

1. **Step 1 (Guest Information)**: Call `/booking/step-1/` to validate guest data and check availability
2. **Step 2 (Payment)**: Call `/booking/step-2/` to validate payment information
3. **Step 3 (Confirmation)**: Call `/booking/step-3/` to create the actual reservation

### Frontend API Calls Example

```javascript
// Step 1: Validate guest information
const validateGuestInfo = async (guestData) => {
  const response = await fetch('/api/reservations/booking/step-1/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(guestData)
  });
  return response.json();
};

// Step 2: Validate payment
const validatePayment = async (paymentData) => {
  const response = await fetch('/api/reservations/booking/step-2/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(paymentData)
  });
  return response.json();
};

// Step 3: Create reservation
const createReservation = async (reservationData) => {
  const response = await fetch('/api/reservations/booking/step-3/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(reservationData)
  });
  return response.json();
};

// Check availability
const checkAvailability = async (availabilityData) => {
  const response = await fetch('/api/reservations/availability/check/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(availabilityData)
  });
  return response.json();
};
```

## Authentication

All endpoints except availability checking require authentication using JWT tokens:

```
Authorization: Bearer <jwt_token>
```

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

Error responses include detailed messages:

```json
{
  "error": "Validation failed",
  "details": {
    "guest_email": ["This field is required."]
  }
}
```
