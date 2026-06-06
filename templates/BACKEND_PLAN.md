# E-CAR HUB - COMPREHENSIVE BACKEND DEVELOPMENT PLAN

## PROJECT OVERVIEW
**Application Name:** E-Car Hub  
**Type:** Automotive Service Platform  
**Location/Market:** Kenya  
**Primary Services:** 
- Car Rentals (luxury vehicles)
- Mechanical Repair Services
- Car Care Products
- Service Bookings

---

## 1. DATABASE DESIGN & ENTITIES

### 1.1 USER MANAGEMENT
**User Table**
```
- user_id (Primary Key, UUID)
- full_name (String, Required)
- email (String, Unique, Required)
- phone_number (String, Optional)
- password_hash (String, Required - bcrypt encrypted)
- user_role (Enum: 'customer', 'admin', 'mechanic') - Default: 'customer'
- account_status (Enum: 'active', 'suspended', 'deleted')
- created_at (Timestamp)
- updated_at (Timestamp)
- is_verified (Boolean - email verification)
- profile_picture_url (String, Optional)
```

**Customer Profile Table**
```
- profile_id (Primary Key, UUID)
- user_id (Foreign Key → User)
- national_id (String, Optional)
- driver_license_number (String, Optional)
- date_of_birth (Date, Optional)
- address (String, Optional)
- city (String, Optional)
- preferred_contact_method (Enum: 'email', 'phone', 'sms')
- total_bookings (Integer)
- loyalty_points (Integer) - for future loyalty program
- created_at (Timestamp)
- updated_at (Timestamp)
```

### 1.2 VEHICLE/FLEET MANAGEMENT
**Vehicle Table**
```
- vehicle_id (Primary Key, UUID)
- make (String) - e.g., BMW
- model (String) - e.g., 7 Series
- year (Integer)
- vehicle_type (Enum: 'luxury_sedan', 'economy', 'suv', 'van', 'truck')
- license_plate (String, Unique)
- vin (String, Unique) - Vehicle Identification Number
- color (String)
- fuel_type (Enum: 'petrol', 'diesel', 'hybrid', 'electric')
- transmission (Enum: 'manual', 'automatic')
- seating_capacity (Integer)
- daily_rental_rate (Decimal) - in Kenyan Shillings (KES)
- condition_status (Enum: 'excellent', 'good', 'fair', 'maintenance_needed')
- availability_status (Enum: 'available', 'rented', 'maintenance', 'retired')
- mileage (Integer)
- last_maintenance_date (Date)
- next_maintenance_due_date (Date)
- insurance_provider (String)
- insurance_expiry_date (Date)
- registration_expiry_date (Date)
- vehicle_image_url (String)
- created_at (Timestamp)
- updated_at (Timestamp)
```

**Vehicle Features Table** (Many-to-Many with Vehicle)
```
- feature_id (Primary Key, UUID)
- vehicle_id (Foreign Key → Vehicle)
- feature_name (String) - e.g., 'GPS Navigation', 'Air Conditioning', 'Leather Seats'
- created_at (Timestamp)
```

**Vehicle Maintenance Log Table**
```
- maintenance_id (Primary Key, UUID)
- vehicle_id (Foreign Key → Vehicle)
- maintenance_date (Date)
- maintenance_type (Enum: 'routine', 'repair', 'inspection')
- description (String)
- cost (Decimal)
- performed_by (String)
- parts_used (String)
- next_maintenance_date (Date)
- created_at (Timestamp)
```

### 1.3 RENTAL/BOOKING SYSTEM
**Rental Booking Table**
```
- booking_id (Primary Key, UUID)
- user_id (Foreign Key → User)
- vehicle_id (Foreign Key → Vehicle)
- booking_reference (String, Unique) - Auto-generated code
- start_date (DateTime)
- end_date (DateTime)
- pickup_location (String)
- dropoff_location (String)
- rental_duration_days (Integer) - Auto-calculated
- daily_rate (Decimal)
- subtotal (Decimal)
- discount_applied (Decimal, Default: 0)
- insurance_charge (Decimal, Optional)
- additional_charges (Decimal, Default: 0)
- total_amount (Decimal)
- payment_status (Enum: 'pending', 'completed', 'failed', 'refunded')
- booking_status (Enum: 'pending', 'confirmed', 'active', 'completed', 'cancelled')
- payment_method (Enum: 'mpesa', 'credit_card', 'bank_transfer', 'cash')
- special_requests (String, Optional)
- driver_contact (String)
- created_at (Timestamp)
- updated_at (Timestamp)
- cancelled_at (Timestamp, Optional)
- cancellation_reason (String, Optional)
```

### 1.4 SERVICE REQUEST SYSTEM
**Service Request Table**
```
- request_id (Primary Key, UUID)
- user_id (Foreign Key → User)
- request_reference (String, Unique) - Auto-generated
- full_name (String)
- phone_number (String)
- service_type (String) - e.g., 'Oil Change', 'Engine Repair', 'Inspection'
- vehicle_details (String) - Description of vehicle
- issue_description (String)
- urgency_level (Enum: 'low', 'medium', 'high', 'emergency')
- preferred_date (Date)
- preferred_time (Time)
- estimated_cost (Decimal, Optional)
- actual_cost (Decimal, Optional)
- request_status (Enum: 'new', 'in_progress', 'completed', 'cancelled')
- assigned_mechanic_id (Foreign Key → User, Optional)
- notes (String, Optional)
- created_at (Timestamp)
- updated_at (Timestamp)
- completed_at (Timestamp, Optional)
```

### 1.5 SERVICES CATALOG
**Service Type Table**
```
- service_id (Primary Key, UUID)
- service_name (String) - e.g., 'Oil and Filter Change', 'Battery Replacement'
- description (String)
- category (Enum: 'routine_maintenance', 'repairs', 'diagnostics', 'inspection')
- estimated_duration_hours (Decimal)
- base_price (Decimal)
- service_status (Enum: 'active', 'inactive')
- image_url (String, Optional)
- created_at (Timestamp)
```

### 1.6 PAYMENTS & TRANSACTIONS
**Payment Table**
```
- payment_id (Primary Key, UUID)
- transaction_id (String, Unique) - From payment provider
- booking_id (Foreign Key → Rental Booking, Optional)
- service_request_id (Foreign Key → Service Request, Optional)
- user_id (Foreign Key → User)
- amount (Decimal)
- currency (String, Default: 'KES')
- payment_method (Enum: 'mpesa', 'credit_card', 'bank_transfer', 'cash')
- payment_status (Enum: 'pending', 'completed', 'failed', 'cancelled')
- payment_provider (String) - e.g., 'Daraja (M-Pesa)', 'Stripe', 'PayPal'
- provider_response (JSON) - Store provider's response
- payment_date (Timestamp)
- created_at (Timestamp)
```

### 1.7 TESTIMONIALS & REVIEWS
**Testimonial Table**
```
- testimonial_id (Primary Key, UUID)
- user_id (Foreign Key → User)
- booking_id (Foreign Key → Rental Booking, Optional)
- service_request_id (Foreign Key → Service Request, Optional)
- rating (Integer, 1-5)
- review_text (String)
- is_featured (Boolean, Default: false)
- is_approved (Boolean, Default: false) - Admin moderation
- created_at (Timestamp)
- approved_at (Timestamp, Optional)
```

---

## 2. CORE FEATURES & FUNCTIONALITY

### 2.1 USER MANAGEMENT
- [x] User Registration (Sign Up)
  - Full name, email, password validation
  - Email verification via OTP or link
  - Role-based registration (customer by default)
  
- [x] User Authentication (Login)
  - Email/password login
  - JWT token generation
  - Session management
  
- [x] Password Management
  - Secure password storage (bcrypt)
  - Password reset via email
  - Change password functionality
  
- [x] User Profile
  - View and update profile information
  - Profile picture upload
  - Driver license & National ID storage (optional)

### 2.2 VEHICLE/FLEET MANAGEMENT
- [x] Vehicle Inventory
  - Add, edit, delete vehicles
  - Set rental rates and daily prices
  - Track vehicle availability status
  
- [x] Vehicle Search & Filtering
  - Filter by: vehicle type, seating capacity, fuel type, price range, availability
  - Search by make/model
  - Show available vehicles with specifications
  
- [x] Vehicle Details
  - Display vehicle features, specifications, pricing
  - Show maintenance history
  - Current availability status
  
- [x] Maintenance Tracking
  - Log maintenance activities
  - Track next maintenance due date
  - Alert when maintenance is overdue
  - Insurance and registration tracking

### 2.3 RENTAL BOOKING SYSTEM
- [x] Create Booking
  - Select vehicle, start/end dates
  - Calculate total cost automatically
  - Apply discounts if applicable
  
- [x] Booking Management
  - View booking history
  - Modify existing bookings (if possible)
  - Cancel bookings with refund logic
  
- [x] Booking Status Tracking
  - Real-time status updates (pending → confirmed → active → completed)
  - Email/SMS notifications at each status change
  
- [x] Invoice Generation
  - Auto-generate invoice for each booking
  - Include breakdown: rental days, daily rate, insurance, discounts, total
  - Send via email

### 2.4 SERVICE REQUEST SYSTEM
- [x] Service Request Form
  - Capture: customer info, vehicle details, issue description, urgency
  - Date/time preferences
  
- [x] Service Management
  - Assign mechanic to service request
  - Track service progress
  - Update estimated and actual costs
  
- [x] Service History
  - Customers can view their service requests
  - Detailed history with dates, costs, notes

### 2.5 PAYMENT INTEGRATION
- [x] Payment Methods
  - M-Pesa (Daraja API) - Kenya's primary payment method
  - Credit/Debit Card (Stripe/PayPal)
  - Bank Transfer
  - Cash Payment (manual tracking)
  
- [x] Payment Processing
  - Secure payment handling
  - Transaction logging
  - Receipt generation
  
- [x] Refund Management
  - Process refunds for cancelled bookings
  - Track refund status

### 2.6 REVIEWS & TESTIMONIALS
- [x] Submit Reviews
  - Rate service (1-5 stars)
  - Write review comments
  
- [x] Testimonial Management
  - Admin approval workflow
  - Display approved testimonials on website
  - Feature popular testimonials

### 2.7 ADMIN DASHBOARD
- [x] Dashboard Overview
  - Total bookings, revenue, pending requests
  - Recent activity feed
  
- [x] Vehicle Management
  - Manage fleet, inventory
  - Track maintenance schedules
  
- [x] Booking Management
  - View all bookings, confirm/cancel
  - Generate reports
  
- [x] User Management
  - View/manage users
  - Suspend/activate accounts
  - View customer history
  
- [x] Service Management
  - Assign mechanics
  - Track service progress
  - Generate service reports
  
- [x] Financial Reports
  - Revenue tracking
  - Payment status reports
  - Outstanding payments

---

## 3. API ENDPOINTS (RESTful Architecture)

### 3.1 AUTHENTICATION ENDPOINTS
```
POST   /api/auth/register        - User registration
POST   /api/auth/login           - User login
POST   /api/auth/logout          - User logout
POST   /api/auth/refresh-token   - Refresh JWT token
POST   /api/auth/forgot-password - Request password reset
POST   /api/auth/reset-password  - Reset password with token
POST   /api/auth/verify-email    - Verify email OTP
```

### 3.2 USER ENDPOINTS
```
GET    /api/users/me             - Get current user profile
PUT    /api/users/me             - Update current user profile
GET    /api/users/{userId}       - Get specific user (admin)
PUT    /api/users/{userId}       - Update user (admin)
DELETE /api/users/{userId}       - Delete user account
POST   /api/users/{userId}/avatar - Upload profile picture
```

### 3.3 VEHICLE ENDPOINTS
```
GET    /api/vehicles             - List all vehicles with filters
GET    /api/vehicles/{vehicleId} - Get vehicle details
POST   /api/vehicles             - Add new vehicle (admin)
PUT    /api/vehicles/{vehicleId} - Update vehicle (admin)
DELETE /api/vehicles/{vehicleId} - Delete vehicle (admin)
GET    /api/vehicles/{vehicleId}/maintenance - Get maintenance history
POST   /api/vehicles/{vehicleId}/maintenance - Log maintenance
GET    /api/vehicles/search      - Search vehicles by criteria
```

### 3.4 RENTAL BOOKING ENDPOINTS
```
POST   /api/bookings             - Create new booking
GET    /api/bookings             - List user's bookings
GET    /api/bookings/{bookingId} - Get booking details
PUT    /api/bookings/{bookingId} - Update booking (if allowed)
DELETE /api/bookings/{bookingId} - Cancel booking
POST   /api/bookings/{bookingId}/invoice - Generate invoice
POST   /api/bookings/{bookingId}/confirm - Confirm booking
GET    /api/bookings/admin/all   - Get all bookings (admin)
```

### 3.5 SERVICE REQUEST ENDPOINTS
```
POST   /api/service-requests         - Create service request
GET    /api/service-requests         - List user's requests
GET    /api/service-requests/{id}    - Get request details
PUT    /api/service-requests/{id}    - Update request
DELETE /api/service-requests/{id}    - Cancel request
POST   /api/service-requests/{id}/assign - Assign mechanic (admin)
GET    /api/service-requests/admin/all - All requests (admin)
```

### 3.6 SERVICES ENDPOINTS
```
GET    /api/services             - List all service types
GET    /api/services/{serviceId} - Get service details
POST   /api/services             - Add service (admin)
PUT    /api/services/{serviceId} - Update service (admin)
DELETE /api/services/{serviceId} - Delete service (admin)
```

### 3.7 PAYMENT ENDPOINTS
```
POST   /api/payments/initiate    - Initiate payment
POST   /api/payments/mpesa-callback - M-Pesa callback handler
GET    /api/payments/{paymentId} - Get payment status
POST   /api/payments/{paymentId}/refund - Process refund
GET    /api/payments/user/history - User payment history
```

### 3.8 TESTIMONIALS ENDPOINTS
```
POST   /api/testimonials         - Submit review/testimonial
GET    /api/testimonials         - Get approved testimonials
GET    /api/testimonials/admin   - All testimonials (admin)
PUT    /api/testimonials/{id}    - Edit testimonial
DELETE /api/testimonials/{id}    - Delete testimonial
POST   /api/testimonials/{id}/approve - Approve testimonial (admin)
```

---

## 4. TECHNICAL STACK RECOMMENDATIONS

### Backend Framework
- **Node.js + Express.js** (Recommended) or **Python + Django/FastAPI** or **Java + Spring Boot**
- Framework should support: JWT, middleware, database ORM

### Database
- **Primary:** PostgreSQL (robust, ACID compliance)
- **Cache:** Redis (session storage, rate limiting)

### Authentication & Security
- **JWT (JSON Web Tokens)** for stateless authentication
- **bcrypt** for password hashing
- **CORS** configuration for frontend integration
- **Rate limiting** to prevent abuse
- **HTTPS/SSL** certificate required

### Payment Integration
- **Daraja (M-Pesa) API** - Primary payment gateway for Kenya
- **Stripe/PayPal SDK** - Alternative payment methods
- **Secure payment token handling**

### Additional Tools
- **Email Service:** SendGrid, Mailgun, or AWS SES (for notifications)
- **SMS Service:** Twilio or Africa's Talking (for OTP, booking notifications)
- **File Storage:** AWS S3 or Firebase Storage (vehicle images, documents)
- **Logging:** Winston, Morgan (request/error logging)
- **Environment Config:** dotenv for configuration management

---

## 5. AUTHENTICATION & SECURITY REQUIREMENTS

### 5.1 Authentication Flow
1. User registers with email & password
2. Email verification link/OTP sent
3. User verifies email
4. User logs in with email & password
5. Backend generates JWT token (access + refresh)
6. Token sent in Authorization header for protected routes
7. Refresh token mechanism for extended sessions

### 5.2 Security Measures
- Password hashing with bcrypt (salt rounds: 12)
- JWT expiration (access: 1 hour, refresh: 7 days)
- CORS whitelist configuration
- SQL injection prevention (use parameterized queries)
- XSS protection headers
- Rate limiting on login endpoints
- Input validation on all endpoints
- Secure password reset flow (time-limited tokens)

### 5.3 Role-Based Access Control (RBAC)
```
CUSTOMER:
  - View own profile
  - Create bookings
  - Submit service requests
  - View own booking/service history
  - Submit reviews

MECHANIC:
  - View assigned service requests
  - Update service progress
  - View customer details

ADMIN:
  - Full access to all resources
  - Manage vehicles & fleet
  - Manage users
  - View financial reports
  - Approve testimonials
  - Manage service types
```

---

## 6. BUSINESS LOGIC & CALCULATIONS

### 6.1 Booking Total Calculation
```
rental_duration_days = end_date - start_date
subtotal = rental_duration_days × daily_rate

discount = calculate_discount() // Based on duration or promo code
insurance_charge = subtotal × insurance_rate (if selected)
additional_charges = late_fee + damage_charge (if any)

total_amount = subtotal - discount + insurance_charge + additional_charges
```

### 6.2 Availability Status Updates
- When booking created → vehicle status = "rented"
- When booking cancelled → vehicle status = "available"
- When maintenance logged → vehicle status = "maintenance"
- Manual admin status updates

### 6.3 Booking Status Flow
```
Pending (booking created)
  ↓ (user confirms payment)
Confirmed (payment received)
  ↓ (rental start date arrives)
Active (customer using vehicle)
  ↓ (rental end date arrives)
Completed (vehicle returned)

Alternative: Cancelled (can happen at any stage with refund logic)
```

### 6.4 Service Request Status Flow
```
New (created)
  ↓ (admin reviews)
In Progress (assigned mechanic, work started)
  ↓ (work completed)
Completed
  ↓ (customer can review)

Alternative: Cancelled (by customer or admin with reason)
```

---

## 7. NOTIFICATIONS & COMMUNICATIONS

### 7.1 Email Notifications
- Welcome email after registration
- Email verification link
- Booking confirmation
- Booking reminder (day before)
- Service request confirmation
- Service completion notification
- Invoice/receipt email
- Payment confirmation
- Password reset instructions

### 7.2 SMS Notifications (Optional)
- Booking confirmation code
- Service appointment reminder
- Payment verification OTP
- Booking/service status updates

---

## 8. REPORTING & ANALYTICS

### 8.1 Admin Reports
- Daily/Monthly/Yearly revenue
- Booking statistics
- Vehicle utilization rate
- Popular services
- Customer satisfaction (average rating)
- Outstanding payments

### 8.2 User Reports
- Personal booking history
- Spending summary
- Service history with costs

---

## 9. ERROR HANDLING & VALIDATION

### 9.1 HTTP Status Codes to Implement
- 200 OK - Successful request
- 201 Created - Resource created
- 400 Bad Request - Invalid input
- 401 Unauthorized - Authentication required
- 403 Forbidden - Permission denied
- 404 Not Found - Resource not found
- 409 Conflict - Resource already exists
- 429 Too Many Requests - Rate limit exceeded
- 500 Internal Server Error

### 9.2 Input Validation
- Email format validation
- Password strength requirements (min 8 chars, uppercase, number, special char)
- Phone number format (Kenyan format: +254...)
- Date validation (future dates for bookings)
- Amount validation (positive numbers)
- File upload validation (image types, size limits)

---

## 10. DEPLOYMENT & INFRASTRUCTURE

### Environment Setup
- **Development:** Local environment with .env file
- **Staging:** Test server for QA
- **Production:** Live server with SSL, backups, monitoring

### Hosting Options
- AWS (EC2, RDS for database)
- Heroku (easier deployment)
- DigitalOcean
- Google Cloud Platform
- Local server with domain

### Database Backups
- Daily automated backups
- Backup retention policy (30+ days)
- Disaster recovery plan

---

## 11. FUTURE ENHANCEMENTS

- Loyalty points program
- Insurance calculator
- GPS tracking for rented vehicles
- Mobile app (iOS/Android)
- Advanced analytics & ML-based recommendations
- Integration with other rental platforms
- Multi-language support
- Dark mode UI

---

## 12. DATA FLOW SUMMARY

### Rental Booking Flow
```
User selects vehicle → 
Views details & price → 
Selects dates → 
Booking created (PENDING) → 
Initiates payment → 
Payment processed → 
Booking status = CONFIRMED → 
Email confirmation & invoice sent → 
Booking date arrives → 
Status = ACTIVE → 
Vehicle returned → 
Status = COMPLETED → 
Can submit review
```

### Service Request Flow
```
User submits service form → 
Request created (NEW) → 
Admin reviews → 
Mechanic assigned → 
Status = IN_PROGRESS → 
Work completed → 
Status = COMPLETED → 
Invoice sent → 
Can submit review
```

---

## SUMMARY FOR AI ASSISTANT

**You are creating a backend for E-Car Hub, a Kenyan automotive platform offering:**

1. **Vehicle Rentals** - Users book luxury cars with availability tracking
2. **Service Bookings** - Customers request mechanical services
3. **User Management** - Registration, authentication, profiles
4. **Payment Processing** - M-Pesa and card payments
5. **Admin Dashboard** - Fleet, booking, and financial management

**The backend must handle:**
- User authentication & RBAC
- Complex booking calculations
- Payment integration (especially M-Pesa for Kenya)
- Email/SMS notifications
- Multi-role authorization
- Real-time availability management
- Financial tracking & reporting

**Tech Stack Preference:** Node.js/Express with PostgreSQL, or your preferred stack that supports the above features.

All data must be normalized, secure, and scalable for a growing user base.
