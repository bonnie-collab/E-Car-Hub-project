# E-CAR HUB BACKEND - QUICK REFERENCE GUIDE

## 🎯 PROJECT AT A GLANCE

**E-Car Hub** is a Kenya-based automotive service platform for:
- 🚗 **Car Rentals** - Book luxury vehicles daily
- 🔧 **Mechanical Services** - Request car repairs
- 👥 **User Management** - Sign up, login, profiles
- 💳 **Payments** - M-Pesa, cards, bank transfers
- 📊 **Admin Dashboard** - Manage fleet, bookings, finances

---

## 📊 DATABASE ENTITIES (8 Main Tables)

| Entity | Purpose | Key Fields |
|--------|---------|-----------|
| **Users** | Customer accounts | email, password, role, verified |
| **Customer Profiles** | Extended user data | national_id, driver_license, address |
| **Vehicles** | Car inventory | make, model, daily_rate, availability |
| **Vehicle Features** | Car specs | GPS, AC, Leather seats (Many-to-Many) |
| **Maintenance Logs** | Service history | date, type, cost, next_due_date |
| **Rental Bookings** | Car rentals | user, vehicle, dates, total_amount |
| **Service Requests** | Repair requests | customer, issue, urgency, assigned_mechanic |
| **Payments** | Transaction logs | amount, method, status, provider_ref |
| **Testimonials** | Reviews | rating, review_text, is_approved |
| **Service Types** | Available services | name, category, base_price |

---

## 🔐 USER ROLES & PERMISSIONS

```
CUSTOMER
├─ View available vehicles
├─ Create bookings
├─ Request services
├─ View own history
├─ Submit reviews
└─ Manage profile

MECHANIC
├─ View assigned requests
├─ Update service progress
├─ View customer details
└─ Complete services

ADMIN
├─ Manage all users
├─ Add/edit/delete vehicles
├─ Approve/reject testimonials
├─ View financial reports
├─ Assign mechanics
└─ Full system access
```

---

## 🔄 MAIN BUSINESS FLOWS

### BOOKING FLOW:
```
1. User selects vehicle
2. Chooses dates
3. System calculates: rental_days × daily_rate - discount + insurance
4. User initiates payment
5. Payment processed (M-Pesa/Card)
6. Booking CONFIRMED
7. Email sent with details
8. Booking date arrives → Status = ACTIVE
9. Return vehicle → Status = COMPLETED
10. Can submit review
```

### SERVICE REQUEST FLOW:
```
1. User submits issue details
2. Admin reviews & assigns mechanic
3. Status = IN_PROGRESS
4. Mechanic completes work
5. Status = COMPLETED
6. Invoice sent
7. User can review/rate
```

---

## 💰 BOOKING COST CALCULATION

```javascript
rental_days = end_date - start_date
subtotal = rental_days × daily_rate

// Apply discount if any
discount = check_promo_code() OR volume_discount()
subtotal_after_discount = subtotal - discount

// Add optional insurance
insurance = subtotal_after_discount × insurance_rate (if selected)

// Add additional charges (if any)
additional = late_fee + damage_charge

TOTAL = subtotal_after_discount + insurance + additional
```

---

## 🌐 API ENDPOINTS (Quick Overview)

### Authentication (7 endpoints)
- Register, Login, Logout, Refresh Token, Forgot Password, Reset Password, Verify Email

### Users (6 endpoints)
- Get Profile, Update Profile, Get User (admin), Update User (admin), Delete User, Upload Avatar

### Vehicles (8 endpoints)
- List Vehicles, Get Details, Add (admin), Edit (admin), Delete (admin), Maintenance History, Log Maintenance, Search

### Bookings (8 endpoints)
- Create, Get My Bookings, Get Details, Update, Cancel, Generate Invoice, Confirm, Get All (admin)

### Service Requests (7 endpoints)
- Create, Get My Requests, Get Details, Update, Delete, Assign Mechanic (admin), Get All (admin)

### Services (6 endpoints)
- List, Get Details, Add (admin), Edit (admin), Delete (admin)

### Payments (5 endpoints)
- Initiate, M-Pesa Callback (webhook), Get Status, Process Refund, Payment History

### Testimonials (7 endpoints)
- Submit, Get Approved, Get All (admin), Edit, Delete, Approve (admin)

---

## 🔐 SECURITY CHECKLIST

- ✅ JWT Authentication (Access: 1hr, Refresh: 7 days)
- ✅ Password hashing with bcrypt (12 rounds)
- ✅ Role-based authorization middleware
- ✅ CORS configuration
- ✅ Input validation on all endpoints
- ✅ SQL injection prevention (parameterized queries)
- ✅ Rate limiting on sensitive endpoints
- ✅ HTTPS/SSL required
- ✅ XSS protection headers
- ✅ Password reset: time-limited tokens (30 min)
- ✅ Email verification required
- ✅ Secure payment handling

---

## 📧 NOTIFICATIONS TO IMPLEMENT

**Email Notifications:**
- Welcome email
- Email verification
- Booking confirmation
- Service confirmation
- Reminders (1 day before)
- Invoice/Receipt
- Payment confirmation
- Service completion
- Password reset

**SMS Notifications (Optional):**
- Booking OTP
- Appointment reminders
- Payment verification

---

## 💳 PAYMENT METHODS

1. **M-Pesa (Daraja API)** - PRIMARY for Kenya ⭐⭐⭐⭐⭐
2. **Credit/Debit Card** - Stripe or PayPal
3. **Bank Transfer** - Manual tracking
4. **Cash** - Manual tracking with receipt

---

## 🛠️ TECH STACK RECOMMENDED

### Backend
- **Node.js + Express** (recommended) 
- OR Python + Django/FastAPI
- OR Java + Spring Boot

### Database
- **PostgreSQL** - Primary database
- **Redis** - Caching & sessions (optional)

### External Services
- **Payment:** Daraja (M-Pesa), Stripe
- **Email:** SendGrid, Mailgun, AWS SES
- **SMS:** Twilio, Africa's Talking
- **Storage:** AWS S3, Firebase Storage
- **Logging:** Winston, Morgan

---

## ✅ KEY FEATURES CHECKLIST

### User Management
- [ ] Registration with email verification
- [ ] Login with JWT
- [ ] Password reset via email
- [ ] Profile management
- [ ] Avatar upload

### Vehicle Management
- [ ] Add/Edit/Delete vehicles
- [ ] Track availability
- [ ] Maintenance scheduling
- [ ] Insurance tracking
- [ ] Search & filtering

### Bookings
- [ ] Create booking with auto-calculation
- [ ] Cancel with refund logic
- [ ] Status tracking
- [ ] Invoice generation
- [ ] Email notifications

### Service Requests
- [ ] Submit request form
- [ ] Mechanic assignment
- [ ] Progress tracking
- [ ] Cost estimation
- [ ] Service history

### Payments
- [ ] M-Pesa integration
- [ ] Card payment integration
- [ ] Transaction logging
- [ ] Receipt generation
- [ ] Refund processing

### Admin Features
- [ ] Dashboard with KPIs
- [ ] User management
- [ ] Vehicle management
- [ ] Financial reports
- [ ] Testimonial approval

---

## 📈 REPORTS TO GENERATE

**Admin Reports:**
- Daily/Monthly/Yearly revenue
- Booking statistics
- Vehicle utilization rate
- Popular services
- Customer satisfaction (avg rating)
- Outstanding payments
- Mechanic performance

---

## 🚀 DEPLOYMENT CONSIDERATIONS

- PostgreSQL database with automated backups
- Environment configuration (.env file)
- Error logging & monitoring
- Rate limiting
- HTTPS/SSL certificate
- API documentation (Swagger/Postman)
- Seed data for testing
- Database migrations

---

## 📝 VALIDATION RULES

### Users
- Email: valid email format, unique
- Password: min 8 chars, uppercase, number, special char
- Phone: Kenya format (+254...)

### Bookings
- Start date must be future
- End date must be after start date
- Vehicle must be available
- Amount must be positive

### Payments
- Amount must match booking total
- Payment method must be valid
- Transaction ID must be unique

### Service Requests
- Issue description required
- Phone number valid format
- Urgency level selected

---

## 🎯 WHAT TO PROVIDE TO GEMINI AI

Use the **GEMINI_PROMPT.md** file to paste the complete requirements into Gemini AI. 

Ask Gemini for:
1. Complete backend API code
2. Database migrations
3. Authentication middleware
4. M-Pesa integration implementation
5. Email notification system
6. RBAC middleware
7. Error handling utilities
8. API documentation
9. .env.example file
10. Seed data file

---

## 📞 CONTACT & FOLLOW-UP QUESTIONS FOR GEMINI

After getting initial code, ask:
- "Can you create unit tests for the payment module?"
- "Show me how to deploy to Heroku"
- "Create Docker setup for development"
- "Add pagination and sorting to list endpoints"
- "Implement request rate limiting"
- "Create monitoring and logging utilities"
- "Add image upload to S3"
- "Set up CI/CD pipeline"

---

## 🔗 FILES IN THIS PROJECT

- **BACKEND_PLAN.md** - Detailed technical specification (this document)
- **GEMINI_PROMPT.md** - Ready-to-paste Gemini AI prompt
- **QUICK_REFERENCE.md** - This file
- Frontend files: index.html, services.html, about.html, etc.

---

**START HERE:** Copy entire content from **GEMINI_PROMPT.md** → Paste into Gemini AI → Get your complete backend! 🚀
