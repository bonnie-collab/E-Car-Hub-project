# E-CAR HUB SYSTEM ARCHITECTURE OVERVIEW

## 🏗️ SYSTEM ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Your Current Code)                    │
│  ┌──────────────┬──────────────┬──────────────┬──────────────────────┐  │
│  │ index.html   │ services.html │ about.html   │ signup/login.html    │  │
│  │ (Home)       │ (Services)    │ (About)      │ (Auth)               │  │
│  └──────────────┴──────────────┴──────────────┴──────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ requestform.html (Booking & Service Request Forms)              │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ style.css (Bootstrap Styling)                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
                          (HTTP/HTTPS Requests)
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                    BACKEND API (TO BE CREATED)                          │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    API GATEWAY / MIDDLEWARE                      │  │
│  │  ├─ Request Validation                                          │  │
│  │  ├─ Authentication (JWT)                                        │  │
│  │  ├─ Authorization (RBAC)                                        │  │
│  │  ├─ Rate Limiting                                               │  │
│  │  └─ CORS Handling                                               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      ROUTE HANDLERS                               │  │
│  │  ┌──────────────┬──────────────┬──────────────┬─────────────┐   │  │
│  │  │ Auth Routes  │ User Routes  │ Vehicle      │ Booking     │   │  │
│  │  │              │              │ Routes       │ Routes      │   │  │
│  │  ├──────────────┼──────────────┼──────────────┼─────────────┤   │  │
│  │  │ Service      │ Payment      │ Testimonial  │ Admin       │   │  │
│  │  │ Routes       │ Routes       │ Routes       │ Routes      │   │  │
│  │  └──────────────┴──────────────┴──────────────┴─────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     BUSINESS LOGIC LAYER                         │  │
│  │  ├─ User Management Service                                      │  │
│  │  ├─ Vehicle Management Service                                   │  │
│  │  ├─ Booking Service (calculation, status management)            │  │
│  │  ├─ Service Request Service                                      │  │
│  │  ├─ Payment Processing Service                                   │  │
│  │  ├─ Email Notification Service                                   │  │
│  │  └─ Admin Dashboard Service                                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     DATABASE ACCESS LAYER                        │  │
│  │  └─ ORM (Sequelize, TypeORM, SQLAlchemy, etc.)                 │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
        ┌───────────────────┬──────────────────┬─────────────┐
        ↓                   ↓                  ↓             ↓
┌─────────────────┐ ┌──────────────────┐ ┌──────────┐ ┌──────────┐
│   PostgreSQL    │ │ Redis (Cache)    │ │ AWS S3   │ │Email SES │
│   Database      │ │ Sessions & Cache │ │ Images   │ │ SendGrid │
└─────────────────┘ └──────────────────┘ └──────────┘ └──────────┘
        ↓                                       ↓
┌─────────────────────────────────────┐ ┌─────────────────┐
│  EXTERNAL PAYMENT GATEWAYS          │ │ SMS SERVICE     │
├─────────────────────────────────────┤ │ Twilio/Africa's │
│ • M-Pesa (Daraja API) - PRIMARY     │ │ Talking         │
│ • Stripe - Alternative              │ └─────────────────┘
│ • PayPal - Alternative              │
└─────────────────────────────────────┘
```

---

## 📊 DATABASE SCHEMA RELATIONSHIPS

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                    USERS TABLE (Core Entity)                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ user_id (PK) | email | password | role | status             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│    ↓                           ↓                    ↓              │
│    │ 1:1                       │ 1:1                │ 1:Many       │
│    ↓                           ↓                    ↓              │
│  ┌──────────────────┐  ┌───────────────────┐  ┌──────────────────┐
│  │CUSTOMER_PROFILE  │  │ RENTAL_BOOKINGS   │  │ SERVICE_REQUESTS │
│  │user_id (FK)      │  │user_id (FK)       │  │user_id (FK)      │
│  │national_id       │  │vehicle_id (FK)    │  │assigned_mech_id  │
│  │driver_license    │  │booking_reference  │  │(FK to User)      │
│  └──────────────────┘  └───────────────────┘  └──────────────────┘
│
│                         VEHICLES TABLE
│                      ┌─────────────────┐
│                      │vehicle_id (PK)  │
│                      │make, model, year │
│                      │daily_rate        │
│                      │availability      │
│                      └─────────────────┘
│                        ↓         ↓
│                        │         │
│       ┌────────────────┼─────────┼────────────────┐
│       ↓                ↓         ↓                ↓
│   ┌─────────┐  ┌──────────────────────┐  ┌──────────────┐
│   │FEATURES │  │ MAINTENANCE_LOGS     │  │RENTAL_BOOKINGS
│   │vehicle_ │  │vehicle_id (FK)       │  │vehicle_id(FK)
│   │id (FK)  │  │maintenance_date      │  │(many bookings)
│   └─────────┘  │type, cost            │  └──────────────┘
│                │next_due_date         │
│                └──────────────────────┘
│
│                    PAYMENTS TABLE
│                  ┌─────────────────────┐
│                  │payment_id (PK)      │
│                  │user_id (FK)         │
│                  │booking_id (FK)      │
│                  │service_request_id   │
│                  │(FK)                 │
│                  │amount, status       │
│                  │payment_method       │
│                  └─────────────────────┘
│
│                 TESTIMONIALS TABLE
│                ┌─────────────────────┐
│                │testimonial_id (PK)  │
│                │user_id (FK)         │
│                │booking_id (FK)      │
│                │rating, review_text  │
│                │is_approved          │
│                └─────────────────────┘
│
│                SERVICE_TYPES TABLE
│               ┌─────────────────────┐
│               │service_id (PK)      │
│               │name, category       │
│               │base_price           │
│               └─────────────────────┘
│
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 REQUEST FLOW EXAMPLE: BOOKING A VEHICLE

```
1. USER FRONTEND:
   ┌─────────────────────────────────────┐
   │ Click "Book Now" on vehicle card    │
   │ Select pickup/dropoff dates         │
   │ Click "Continue"                    │
   └──────────────┬──────────────────────┘
                  ↓
2. FRONTEND SENDS HTTP REQUEST:
   ┌──────────────────────────────────────────┐
   │ POST /api/bookings                       │
   │ Body: {                                  │
   │   vehicleId: "uuid...",                  │
   │   startDate: "2024-06-15",               │
   │   endDate: "2024-06-20",                 │
   │   pickupLocation: "Nairobi",             │
   │   dropoffLocation: "Nairobi"             │
   │ }                                        │
   │ Header: Authorization: "Bearer jwt..."   │
   └──────────────┬──────────────────────────┘
                  ↓
3. BACKEND RECEIVES REQUEST:
   ┌──────────────────────────────────────┐
   │ Route Handler: POST /api/bookings    │
   │ Middleware checks:                   │
   │ ✓ JWT token valid?                   │
   │ ✓ User authenticated?                │
   │ ✓ User role: CUSTOMER?               │
   │ ✓ Request data valid?                │
   └──────────────┬──────────────────────┘
                  ↓
4. BUSINESS LOGIC LAYER:
   ┌──────────────────────────────────────┐
   │ BookingService.createBooking():      │
   │ • Fetch vehicle details              │
   │ • Check availability                 │
   │ • Calculate cost:                    │
   │   - rental_days = 5                  │
   │   - daily_rate = 8500 KES            │
   │   - subtotal = 42500 KES             │
   │   - discount = 0 (no promo)          │
   │   - insurance = 1276 KES (3%)        │
   │   - total = 43776 KES                │
   │ • Create booking record              │
   │ • Status: PENDING                    │
   └──────────────┬──────────────────────┘
                  ↓
5. DATABASE LAYER:
   ┌──────────────────────────────────────┐
   │ INSERT INTO rental_bookings:         │
   │ {                                    │
   │   booking_id: "new-uuid",            │
   │   user_id: "customer-uuid",          │
   │   vehicle_id: "vehicle-uuid",        │
   │   booking_reference: "EAR20240615001"│
   │   start_date: "2024-06-15 08:00",    │
   │   end_date: "2024-06-20 08:00",      │
   │   total_amount: 43776,               │
   │   payment_status: "PENDING",         │
   │   booking_status: "PENDING",         │
   │   created_at: now()                  │
   │ }                                    │
   │                                      │
   │ UPDATE vehicles SET:                 │
   │   availability = 'pending_payment'   │
   └──────────────┬──────────────────────┘
                  ↓
6. SEND RESPONSE TO FRONTEND:
   ┌───────────────────────────────────────┐
   │ HTTP 201 Created                      │
   │ {                                     │
   │   success: true,                      │
   │   booking: {                          │
   │     bookingId: "new-uuid",            │
   │     bookingReference: "EAR20240615001"│
   │     totalAmount: 43776,               │
   │     paymentStatus: "PENDING",         │
   │     message: "Booking created.        │
   │              Proceed to payment"      │
   │   }                                   │
   │ }                                     │
   └──────────────┬──────────────────────┘
                  ↓
7. FRONTEND RECEIVES & REDIRECTS:
   ┌───────────────────────────────────────┐
   │ Show success message                  │
   │ Display booking reference             │
   │ Redirect to payment page              │
   │ Show payment options:                 │
   │ • M-Pesa                              │
   │ • Credit Card                         │
   │ • Bank Transfer                       │
   └─────────────────────────────────────  ┘
                  ↓
8. PAYMENT PROCESSING:
   ┌────────────────────────────────────────┐
   │ User selects M-Pesa                    │
   │ Frontend sends: POST /api/payments/    │
   │ initiate with booking_id               │
   │                                        │
   │ Backend triggers M-Pesa Daraja flow    │
   │ M-Pesa prompt sent to user's phone     │
   │ User enters M-Pesa PIN                 │
   │                                        │
   │ M-Pesa → Daraja API → Backend webhook  │
   │ Payment confirmed ✓                    │
   │                                        │
   │ Backend updates:                       │
   │ • Payment status: COMPLETED            │
   │ • Booking status: CONFIRMED            │
   │ • Vehicle availability: RENTED         │
   │ • Send confirmation email              │
   │ • Send invoice PDF                     │
   └────────────────────────────────────────┘
                  ↓
9. NOTIFICATION SENT:
   ┌────────────────────────────────────────┐
   │ Email Subject: Your E-Car Hub          │
   │ Booking Confirmed!                     │
   │                                        │
   │ Dear Customer,                         │
   │ Your booking is confirmed!             │
   │ Reference: EAR20240615001              │
   │ Vehicle: BMW 7 Series 2024             │
   │ Pickup: 2024-06-15 08:00 AM            │
   │ Dropoff: 2024-06-20 08:00 AM           │
   │ Total Amount: KES 43,776               │
   │ Invoice attached                       │
   └────────────────────────────────────────┘
```

---

## 🔐 AUTHENTICATION & AUTHORIZATION FLOW

```
┌──────────────────────────────────┐
│   USER SIGNUP/LOGIN              │
│ ┌────────────────────────────────┐
│ │ 1. Frontend: POST /auth/login  │
│ │    {email, password}           │
│ └─────────────┬──────────────────┘
│               ↓
│ ┌────────────────────────────────┐
│ │ 2. Backend:                    │
│ │    - Find user by email        │
│ │    - Verify password (bcrypt)  │
│ │    - If valid...               │
│ └─────────────┬──────────────────┘
│               ↓
│ ┌────────────────────────────────┐
│ │ 3. Generate JWT Tokens:        │
│ │                                │
│ │ ACCESS TOKEN (1 hour):         │
│ │ Header.Payload.Signature       │
│ │ Payload: {                     │
│ │   userId: "123",               │
│ │   email: "user@email.com",     │
│ │   role: "customer",            │
│ │   iat: 1234567890,             │
│ │   exp: 1234571490              │
│ │ }                              │
│ │                                │
│ │ REFRESH TOKEN (7 days):        │
│ │ Payload: {                     │
│ │   userId: "123",               │
│ │   type: "refresh",             │
│ │   iat: 1234567890,             │
│ │   exp: 1234912690              │
│ │ }                              │
│ └─────────────┬──────────────────┘
│               ↓
│ ┌────────────────────────────────┐
│ │ 4. Send to Frontend:           │
│ │ HTTP 200 OK {                  │
│ │   accessToken: "eyJ...",       │
│ │   refreshToken: "eyJ...",      │
│ │   user: {                      │
│ │     id: "123",                 │
│ │     email: "user@email.com",   │
│ │     role: "customer"           │
│ │   }                            │
│ │ }                              │
│ └─────────────┬──────────────────┘
│               ↓
│ ┌────────────────────────────────┐
│ │ 5. Frontend stores tokens in:  │
│ │    - localStorage or           │
│ │    - sessionStorage or         │
│ │    - secure HttpOnly cookie    │
│ └─────────────┬──────────────────┘
│               ↓
│ ┌────────────────────────────────┐
│ │ 6. For subsequent requests:    │
│ │    Header: {                   │
│ │     Authorization: "Bearer     │
│ │     eyJ..."                    │
│ │    }                           │
│ └─────────────┬──────────────────┘
│               ↓
│ ┌────────────────────────────────┐
│ │ 7. Backend middleware checks:  │
│ │    - Token exists?             │
│ │    - Token not expired?        │
│ │    - Signature valid?          │
│ │    - Extract userId & role     │
│ │    - Attach to request         │
│ └─────────────┬──────────────────┘
│               ↓
│ ┌────────────────────────────────┐
│ │ 8. RBAC Authorization:         │
│ │    if route === "/admin/*":    │
│ │      if user.role !== "admin": │
│ │        return 403 Forbidden    │
│ │    else: continue              │
│ └──────────────────────────────────┘
│
│ When token expires:
│ ┌─────────────────────────────────┐
│ │ Frontend sends refresh token    │
│ │ POST /auth/refresh-token        │
│ │ Backend validates & issues new  │
│ │ access token (reset 1hr timer)  │
│ └─────────────────────────────────┘
└──────────────────────────────────┘
```

---

## 💳 PAYMENT FLOW (M-PESA PRIMARY)

```
┌─────────────────────────────────────────────────────────────┐
│                M-PESA PAYMENT FLOW (Daraja)                 │
│                                                             │
│  1. FRONTEND:                                               │
│     User selects M-Pesa → Enters phone number               │
│     Sends: POST /api/payments/initiate                      │
│     Body: {bookingId, amount, phone_number}                │
│     ↓                                                       │
│  2. BACKEND - /api/payments/initiate:                      │
│     - Validate booking exists                              │
│     - Get Daraja credentials                               │
│     - Prepare M-Pesa request:                              │
│     {                                                       │
│       "BusinessShortCode": "174379",                        │
│       "Password": "base64encoded...",                       │
│       "Timestamp": "20240615145330",                        │
│       "TransactionType": "CustomerPayBillOnline",           │
│       "Amount": 43776,                                      │
│       "PartyA": "254712345678",  (customer phone)           │
│       "PartyB": "174379",         (business code)           │
│       "PhoneNumber": "254712345678",                        │
│       "CallBackURL": "https://backend/api/payments/        │
│                      mpesa-callback",                      │
│       "AccountReference": "EAR20240615001",                │
│       "TransactionDesc": "E-Car Hub Booking"                │
│     }                                                       │
│     ↓                                                       │
│  3. REQUEST M-PESA API:                                    │
│     POST to M-Pesa (Daraja)                               │
│     M-Pesa sends prompt to user's phone                    │
│     ↓                                                       │
│  4. USER INTERACTION:                                      │
│     User receives M-Pesa prompt                            │
│     Enters M-Pesa PIN                                      │
│     Payment processed                                      │
│     ↓                                                       │
│  5. M-PESA → DARAJA → BACKEND WEBHOOK:                    │
│     M-Pesa sends callback to:                              │
│     POST /api/payments/mpesa-callback                      │
│     Callback body contains:                                │
│     {                                                       │
│       "Result": {                                           │
│         "ResultCode": 0,  (0 = success)                    │
│         "ResultDesc": "The service was successful.",        │
│         "OriginatorConversationID": "16114...",             │
│         "ConversationID": "AG_20240615...",                 │
│         "TransactionID": "LEG51X8V60",                      │
│         "ResultParameters": {                               │
│           "ResultParameter": [                              │
│             {                                               │
│               "Key": "Amount",                              │
│               "Value": 43776                                │
│             },                                              │
│             {                                               │
│               "Key": "MpesaReceiptNumber",                  │
│               "Value": "LEG51X8V60"                         │
│             },                                              │
│             {                                               │
│               "Key": "TransactionDate",                     │
│               "Value": "20240615145530"                     │
│             },                                              │
│             {                                               │
│               "Key": "PhoneNumber",                         │
│               "Value": "254712345678"                       │
│             }                                               │
│           ]                                                 │
│         }                                                   │
│       }                                                     │
│     }                                                       │
│     ↓                                                       │
│  6. BACKEND VERIFIES & UPDATES:                           │
│     if ResultCode === 0:                                   │
│       - Log payment to database                            │
│       - Update booking status to CONFIRMED                │
│       - Update vehicle availability to RENTED              │
│       - Create Payment record                              │
│       - Send confirmation email                            │
│       - Return 200 OK to M-Pesa                            │
│     else:                                                   │
│       - Log error                                           │
│       - Update booking status to FAILED                    │
│       - Send error email to customer                       │
│       ↓                                                     │
│  7. CUSTOMER GETS NOTIFICATION:                            │
│     M-Pesa SMS: Payment confirmed                          │
│     Email: Booking confirmation + Invoice                 │
│     Frontend: Success page displayed                       │
│                                                             │
│     BOOKING LIFECYCLE:                                      │
│     PENDING (after booking) →                              │
│     PAYMENT PROCESSING →                                   │
│     CONFIRMED (payment received) →                         │
│     ACTIVE (on booking date) →                             │
│     COMPLETED (after return)                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 DATA ENTITY RELATIONSHIPS

```
ONE-TO-MANY Relationships:
┌─────────────────────────────────────┐
│ One USER has MANY:                  │
│  • Bookings                         │
│  • Service Requests                 │
│  • Payments                         │
│  • Testimonials                     │
│  • One Customer Profile             │
└─────────────────────────────────────┘

┌──────────────────────────────────────┐
│ One VEHICLE has MANY:                │
│  • Rental Bookings                   │
│  • Maintenance Logs                  │
│  • Features (vehicle-to-features M:M)│
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ One SERVICE_TYPE has MANY:           │
│  • Service Requests                  │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ One BOOKING has MANY:                │
│  • Payments                          │
│  • Testimonials                      │
└──────────────────────────────────────┘

MANY-TO-MANY Relationships:
┌──────────────────────────────────────┐
│ VEHICLES ↔ FEATURES                  │
│ (through vehicle_features table)     │
└──────────────────────────────────────┘
```

---

## 🎯 SUMMARY

This architecture ensures:
- ✅ Scalability (can handle growing users)
- ✅ Security (JWT, password hashing, RBAC)
- ✅ Reliability (database transactions, error handling)
- ✅ Maintainability (layered architecture)
- ✅ Extensibility (easy to add new features)
- ✅ Kenya-focused (M-Pesa integration)

**Next Step:** Use the **GEMINI_PROMPT.md** to get Gemini AI to implement this entire architecture! 🚀
