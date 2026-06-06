# GEMINI AI PROMPT - E-CAR HUB BACKEND DEVELOPMENT

Copy and paste this entire prompt into Gemini AI to get started with backend development:

---

## PROMPT FOR GEMINI AI:

I need you to create a complete backend API for an automotive service platform called "E-Car Hub" based in Kenya. Here's the full scope:

### PROJECT OVERVIEW:
E-Car Hub is an automotive platform that provides:
1. **Car Rentals** - Users rent luxury vehicles for daily rates
2. **Service Bookings** - Customers request mechanical repair services
3. **Fleet Management** - Admin manages vehicle inventory
4. **Payment Processing** - Integration with M-Pesa (Kenya), credit cards
5. **User Management** - Customer accounts and admin dashboard

### DATABASE STRUCTURE:

#### User Table
- user_id (UUID, Primary Key)
- full_name, email (unique), phone_number
- password_hash (bcrypt encrypted)
- user_role (customer, admin, mechanic)
- account_status (active, suspended, deleted)
- is_verified (email verification flag)
- profile_picture_url
- created_at, updated_at timestamps

#### Customer Profile Table
- profile_id (UUID)
- user_id (FK), national_id, driver_license_number
- address, city, date_of_birth
- preferred_contact_method
- loyalty_points, total_bookings
- created_at, updated_at

#### Vehicle Table
- vehicle_id (UUID)
- make, model, year, vehicle_type (luxury_sedan, economy, suv, van)
- license_plate (unique), vin (unique)
- fuel_type (petrol, diesel, hybrid, electric)
- transmission, seating_capacity
- daily_rental_rate (in KES), condition_status
- availability_status (available, rented, maintenance, retired)
- mileage, last_maintenance_date, next_maintenance_due_date
- insurance_provider, insurance_expiry_date
- registration_expiry_date
- vehicle_image_url
- created_at, updated_at

#### Vehicle Features Table (Many-to-Many)
- feature_id (UUID), vehicle_id (FK)
- feature_name (e.g., GPS, Air Conditioning, Leather Seats)

#### Vehicle Maintenance Log Table
- maintenance_id (UUID), vehicle_id (FK)
- maintenance_date, maintenance_type (routine, repair, inspection)
- description, cost, performed_by
- parts_used, next_maintenance_date
- created_at

#### Rental Booking Table
- booking_id (UUID), user_id (FK), vehicle_id (FK)
- booking_reference (auto-generated unique code)
- start_date, end_date, rental_duration_days (auto-calculated)
- pickup_location, dropoff_location
- daily_rate, subtotal, discount_applied, insurance_charge
- additional_charges, total_amount
- payment_status (pending, completed, failed, refunded)
- booking_status (pending, confirmed, active, completed, cancelled)
- payment_method (mpesa, credit_card, bank_transfer, cash)
- special_requests, driver_contact
- created_at, updated_at, cancelled_at, cancellation_reason

#### Service Request Table
- request_id (UUID), user_id (FK)
- request_reference (auto-generated unique code)
- full_name, phone_number
- service_type (Oil Change, Engine Repair, etc.)
- vehicle_details, issue_description
- urgency_level (low, medium, high, emergency)
- preferred_date, preferred_time
- estimated_cost, actual_cost
- request_status (new, in_progress, completed, cancelled)
- assigned_mechanic_id (FK to User, optional)
- notes
- created_at, updated_at, completed_at

#### Service Type Table
- service_id (UUID)
- service_name, description
- category (routine_maintenance, repairs, diagnostics, inspection)
- estimated_duration_hours, base_price
- service_status (active, inactive)
- image_url
- created_at

#### Payment Table
- payment_id (UUID), transaction_id (unique)
- booking_id (FK, optional), service_request_id (FK, optional), user_id (FK)
- amount (in KES), payment_method
- payment_status (pending, completed, failed, cancelled)
- payment_provider (Daraja/M-Pesa, Stripe, PayPal)
- provider_response (store provider's JSON response)
- payment_date
- created_at

#### Testimonial Table
- testimonial_id (UUID), user_id (FK)
- booking_id (FK, optional), service_request_id (FK, optional)
- rating (1-5), review_text
- is_featured, is_approved (for admin moderation)
- created_at, approved_at

### CORE FEATURES TO IMPLEMENT:

#### 1. Authentication & User Management
- User registration (email verification required)
- User login (JWT token-based)
- Password reset via email
- Change password functionality
- User profile management
- Role-based access control (Customer, Mechanic, Admin)

#### 2. Vehicle Management
- List all available vehicles with filters (type, price range, seats, fuel type)
- Vehicle details page
- Admin: Add, edit, delete vehicles
- Track vehicle maintenance schedules
- Vehicle availability status management
- Insurance and registration tracking

#### 3. Rental Booking System
- Create booking (select vehicle, dates, calculate total)
- Booking calculations: 
  ```
  rental_duration_days = end_date - start_date
  subtotal = rental_duration_days × daily_rate
  discount = apply_promotional_discount()
  insurance_charge = subtotal × insurance_rate (if selected)
  total = subtotal - discount + insurance_charge + additional_charges
  ```
- Booking status flow: PENDING → CONFIRMED → ACTIVE → COMPLETED (or CANCELLED)
- Cancel booking with refund logic
- View booking history
- Generate invoice/receipt

#### 4. Service Request System
- Customers submit service requests
- Admin assigns mechanics
- Track service progress
- Service status flow: NEW → IN_PROGRESS → COMPLETED (or CANCELLED)
- Service history for customers

#### 5. Payment Integration
- M-Pesa (Daraja) integration (PRIMARY - Kenya market)
- Credit/Debit card payments (Stripe/PayPal)
- Bank transfer option
- Cash payment manual tracking
- Transaction logging and receipt generation
- Refund processing for cancellations
- Payment status tracking

#### 6. Reviews & Testimonials
- Users submit reviews/ratings after bookings or services
- Admin approval workflow
- Featured testimonials functionality
- Display on website

#### 7. Admin Dashboard
- Overview: Total bookings, revenue, pending requests
- Vehicle inventory management
- Booking management (view all, confirm, cancel, generate reports)
- User management (view, suspend, delete accounts)
- Service management (assign mechanics, track progress)
- Financial reports (revenue, payments, outstanding)
- Approval workflow for testimonials

### API ENDPOINTS (RESTful):

**Authentication**
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/refresh-token
- POST /api/auth/forgot-password
- POST /api/auth/reset-password
- POST /api/auth/verify-email

**Users**
- GET /api/users/me
- PUT /api/users/me
- GET /api/users/{userId}
- PUT /api/users/{userId}
- DELETE /api/users/{userId}
- POST /api/users/{userId}/avatar

**Vehicles**
- GET /api/vehicles (with filters)
- GET /api/vehicles/{vehicleId}
- POST /api/vehicles (admin)
- PUT /api/vehicles/{vehicleId} (admin)
- DELETE /api/vehicles/{vehicleId} (admin)
- GET /api/vehicles/{vehicleId}/maintenance
- POST /api/vehicles/{vehicleId}/maintenance (admin)

**Rental Bookings**
- POST /api/bookings
- GET /api/bookings
- GET /api/bookings/{bookingId}
- PUT /api/bookings/{bookingId}
- DELETE /api/bookings/{bookingId}
- POST /api/bookings/{bookingId}/invoice
- POST /api/bookings/{bookingId}/confirm
- GET /api/bookings/admin/all (admin)

**Service Requests**
- POST /api/service-requests
- GET /api/service-requests
- GET /api/service-requests/{id}
- PUT /api/service-requests/{id}
- DELETE /api/service-requests/{id}
- POST /api/service-requests/{id}/assign (admin)
- GET /api/service-requests/admin/all (admin)

**Services**
- GET /api/services
- GET /api/services/{serviceId}
- POST /api/services (admin)
- PUT /api/services/{serviceId} (admin)
- DELETE /api/services/{serviceId} (admin)

**Payments**
- POST /api/payments/initiate
- POST /api/payments/mpesa-callback (webhook)
- GET /api/payments/{paymentId}
- POST /api/payments/{paymentId}/refund
- GET /api/payments/user/history

**Testimonials**
- POST /api/testimonials
- GET /api/testimonials (only approved)
- GET /api/testimonials/admin (all, admin only)
- PUT /api/testimonials/{id}
- DELETE /api/testimonials/{id}
- POST /api/testimonials/{id}/approve (admin)

### SECURITY & AUTHENTICATION:

1. **JWT Authentication**
   - Access token: 1 hour expiration
   - Refresh token: 7 days expiration
   - Tokens in Authorization header: "Bearer {token}"

2. **Password Security**
   - Hash with bcrypt (12 salt rounds)
   - Password requirements: min 8 chars, uppercase, number, special character
   - Password reset: time-limited token (30 min expiration)

3. **Authorization**
   - Role-based access control (CUSTOMER, MECHANIC, ADMIN)
   - Middleware to check roles on protected endpoints
   - CORS configuration for frontend domain

4. **Data Protection**
   - SQL injection prevention (parameterized queries)
   - XSS protection headers
   - Rate limiting (especially on login/payment endpoints)
   - HTTPS/SSL certificate required
   - Input validation on all endpoints

### NOTIFICATIONS:

Email notifications for:
- Welcome email after registration
- Email verification link
- Booking confirmation
- Booking reminder (1 day before)
- Booking status updates
- Service request confirmation
- Service completion
- Invoice/receipt
- Payment confirmation
- Password reset instructions

### ERROR HANDLING:

Implement proper HTTP status codes:
- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict
- 429 Too Many Requests
- 500 Internal Server Error

### TECHNICAL REQUIREMENTS:

- Backend Framework: **Python + Flask** (lightweight, flexible, perfect for this API)
- Database: PostgreSQL with proper indexing
- Authentication: JWT (JSON Web Tokens)
- Password Hashing: bcrypt
- ORM: SQLAlchemy (for database operations)
- Payment Gateway: Daraja (M-Pesa) API integration
- Email Service: SendGrid, Mailgun, or AWS SES (with Flask-Mail)
- SMS Service: Twilio or Africa's Talking (for OTP)
- File Storage: AWS S3 or Firebase (for vehicle images)
- Logging: Python logging module or Python-Logstash
- Environment Variables: python-dotenv for config
- Cache: Redis (optional, for sessions and rate limiting)
- HTTP Client: requests library (for external APIs)
- Additional Python Packages: Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS, Flask-RESTful

### ADDITIONAL NOTES:

- Kenya-specific: Focus on M-Pesa payment integration as primary method
- Ensure scalability for growing user base
- Implement proper error logging and monitoring
- Add request/response validation
- Create comprehensive API documentation
- Include seed data for testing (sample vehicles, services)
- Add pagination for list endpoints
- Implement search and advanced filtering

### DELIVERABLES EXPECTED:

1. Complete API backend with all endpoints
2. Database schema with migrations
3. Authentication system with JWT
4. Payment gateway integration (M-Pesa primary)
5. Email notification system
6. Role-based access control middleware
7. Error handling and logging
8. API documentation (Postman collection or Swagger)
9. Environment configuration template (.env.example)
10. Database seed file with sample data

Please create a production-ready backend that can be deployed and integrated with the frontend. Include proper error handling, validation, and security measures throughout.

---

## INSTRUCTIONS FOR USE:

1. Copy the entire "PROMPT FOR GEMINI AI" section above
2. Go to https://gemini.google.com
3. Paste it into a new chat
4. Wait for Gemini to provide the complete backend code
5. You can ask follow-up questions like:
   - "Can you provide the database migrations?"
   - "Give me the authentication middleware code"
   - "Show me the M-Pesa integration implementation"
   - "Provide Postman collection for API testing"
   - "Create seed data for testing"
