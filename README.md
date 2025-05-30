# 🧩 Dokumentacja API – Moduł Gospodarzy (DreamBook)

Backend systemu rezerwacji DreamBook – moduł Gospodarzy. Poniżej znajduje się dokumentacja REST API dla wszystkich zasobów tego modułu.

---

## 🔗 Endpointy

### 1. Gospodarze (Hosts)
- `GET /api/hosts/` – lista gospodarzy
- `POST /api/hosts/` – dodanie gospodarza
- `GET /api/hosts/{id}/` – szczegóły gospodarza
- `PUT /api/hosts/{id}/` – edycja gospodarza
- `DELETE /api/hosts/{id}/` – usunięcie gospodarza

#### Pola:
- `id`: int
- `name`: string
- `location`: string
- `rating`: float
- `image`: URL

---

### 2. Dostępność (`HostAvailability`)
- `GET /api/host-availability/`
- `POST /api/host-availability/`

#### Pola:
- `host`: FK
- `start_date`: YYYY-MM-DD
- `end_date`: YYYY-MM-DD

---

### 3. Rezerwacje (`HostBooking`)
- `GET /api/host-bookings/`
- `POST /api/host-bookings/`

#### Pola:
- `host`: FK
- `reservation_id`: int
- `booking_date`: YYYY-MM-DD

---

### 4. Wiadomości (`HostMessage`)
- `GET /api/host-messages/`
- `POST /api/host-messages/`

#### Pola:
- `host`: FK
- `user_id`: int
- `message_text`: string
- `sent_date`: auto

---

### 5. Promocje (`HostPromotion`)
- `GET /api/host-promotions/`
- `POST /api/host-promotions/`

#### Pola:
- `host`: FK
- `promotion_details`: string
- `start_date`: YYYY-MM-DD
- `end_date`: YYYY-MM-DD

---

### 6. Statystyki (`HostStatistics`)
- `GET /api/host-statistics/`
- `POST /api/host-statistics/`

#### Pola:
- `host`: FK
- `total_reservations`: int
- `total_earnings`: decimal

---

### 7. Zarobki (`HostEarnings`)
- `GET /api/host-earnings/`
- `POST /api/host-earnings/`

#### Pola:
- `host`: FK
- `earnings_amount`: decimal
- `earnings_date`: YYYY-MM-DD

---

### 8. Polityka rezerwacji (`HostReservationPolicy`)
- `GET /api/host-reservation-policy/`
- `POST /api/host-reservation-policy/`

#### Pola:
- `host`: FK
- `cancellation_policy`: string

---

### 9. Powiadomienia (`HostNotification`)
- `GET /api/host-notifications/`
- `POST /api/host-notifications/`

#### Pola:
- `host`: FK
- `notification_type`: string
- `notification_date`: auto

---

### 10. Wsparcie (`HostSupport`)
- `GET /api/host-support/`
- `POST /api/host-support/`

#### Pola:
- `host`: FK
- `issue_description`: string
- `status`: enum(`new`, `in_progress`, `closed`)

---

## 🧪 Testowanie
Możesz testować wszystkie endpointy:
- przez przeglądarkę (Django REST Framework UI)
- przez Postman / curl
- lub za pomocą `python manage.py test hosts`

---

## 📌 Uwagi
- Wszystkie dane są obsługiwane przez Django REST Framework `ModelViewSet`
- Wszystkie endpointy wspierają `GET`, `POST`, `PUT`, `DELETE` (o ile nie zaznaczono inaczej)

# 🗺️ Dokumentacja API – Moduł Mapy (DreamBook)

Backend systemu DreamBook – funkcje obsługujące interaktywną mapę i lokalizacje.

---

## 🔗 Endpointy

### 1. Lokalizacje (`Location`)
- `GET /api/locations/`
- `POST /api/locations/`
- `PUT /api/locations/{id}/`
- `DELETE /api/locations/{id}/`

#### Pola:
- `id`: int
- `name`: string
- `location`: string
- `latitude`: float
- `longitude`: float

---

### 2. Znaczniki (`MapMarker`)
- `GET /api/map-markers/`
- `POST /api/map-markers/`

#### Pola:
- `location`: FK do Location
- `marker_type`: enum (`property`, `poi`, `custom`)
- `label`: string

---

### 3. Punkty zainteresowania (`POI`)
- `GET /api/pois/`
- `POST /api/pois/`

#### Pola:
- `name`: string
- `description`: string
- `location`: FK do Location

---

### 4. Adnotacje (`MapAnnotation`)
- `GET /api/map-annotations/`
- `POST /api/map-annotations/`

#### Pola:
- `location`: FK do Location
- `text`: string

---

### 5. Zakładki (`MapBookmark`)
- `GET /api/map-bookmarks/`
- `POST /api/map-bookmarks/`

#### Pola:
- `user_id`: int
- `location`: FK do Location

---

## 🧪 Testowanie

- Interfejs REST: `/api/*`
- W pełni kompatybilne z Postman / curl / przeglądarką DRF
- Wspiera `GET`, `POST`, `PUT`, `DELETE` (gdzie dotyczy)

---

## 📌 Uwagi

- Wszystkie modele powiązane z `Location`
- Obsługiwane przez `ModelViewSet` (Django REST Framework)
- Możliwość rozszerzenia o warstwy map, filtry, clustering