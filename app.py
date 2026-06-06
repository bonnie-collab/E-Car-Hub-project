import os
import uuid
import random
import string
from datetime import datetime, timedelta

from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from flask_cors import CORS

app = Flask(__name__)

# ==========================================
# ⚙️ DATABASE CONNECTION CONFIG (MySQL phpMyAdmin)
# ==========================================
# Assuming standard XAMPP or local installation details. Adjust password if one is set.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ecarhub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ecarhub-super-secret-key-2026'
app.config['JWT_SECRET_KEY'] = 'jwt-secure-secret-key-2026'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# ==========================================
# 🛠️ HELPER SYSTEM UTILITIES
# ==========================================
def generate_uuid():
    return str(uuid.uuid4())

def generate_reference(prefix="ECH"):
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{random_str}-{datetime.now().year}"

def role_required(allowed_roles):
    def decorator(fn):
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') not in allowed_roles:
                return jsonify({"error": f"Forbidden. Requires one of these roles: {allowed_roles}"}), 403
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator

# ==========================================
# 📊 ORM MODELS MAPPED TO PHPMYADMIN TABLES
# ==========================================

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Enum('customer', 'admin', 'mechanic'), default='customer')
    account_status = db.Column(db.Enum('active', 'suspended', 'deleted'), default='active')
    is_verified = db.Column(db.Boolean, default=False)
    profile_picture_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    vehicle_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    vehicle_type = db.Column(db.Enum('luxury_sedan', 'economy', 'suv', 'van'), default='economy')
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    vin = db.Column(db.String(30), unique=True, nullable=False)
    fuel_type = db.Column(db.Enum('petrol', 'diesel', 'hybrid', 'electric'), default='electric')
    daily_rental_rate = db.Column(db.Numeric(10, 2), nullable=False)
    availability_status = db.Column(db.Enum('available', 'rented', 'maintenance', 'retired'), default='available')

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    vehicle_id = db.Column(db.String(36), db.ForeignKey('vehicles.vehicle_id'), nullable=False)
    booking_reference = db.Column(db.String(20), unique=True, default=lambda: generate_reference("BK"))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    rental_duration_days = db.Column(db.Integer, nullable=False)
    daily_rate = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    discount_applied = db.Column(db.Numeric(10, 2), default=0.00)
    insurance_charge = db.Column(db.Numeric(10, 2), default=0.00)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'completed', 'failed', 'refunded'), default='pending')
    booking_status = db.Column(db.Enum('pending', 'confirmed', 'active', 'completed', 'cancelled'), default='pending')
    payment_method = db.Column(db.Enum('mpesa', 'credit_card', 'bank_transfer', 'cash'), default='mpesa')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    request_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    request_reference = db.Column(db.String(20), unique=True, default=lambda: generate_reference("SR"))
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    vehicle_details = db.Column(db.String(255), nullable=False)
    issue_description = db.Column(db.Text)
    urgency_level = db.Column(db.Enum('low', 'medium', 'high', 'emergency'), default='medium')
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.Time, nullable=False)
    estimated_cost = db.Column(db.Numeric(10, 2), nullable=False)
    request_status = db.Column(db.Enum('new', 'in_progress', 'completed', 'cancelled'), default='new')
    assigned_mechanic_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    booking_id = db.Column(db.String(36), db.ForeignKey('bookings.booking_id'), nullable=True)
    service_request_id = db.Column(db.String(36), db.ForeignKey('service_requests.request_id'), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'completed', 'failed', 'cancelled'), default='pending')
    payment_provider = db.Column(db.Enum('Daraja/M-Pesa', 'Stripe', 'PayPal'), default='Daraja/M-Pesa')
    provider_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = User.query.get(identity)
    if user:
        return {"role": user.user_role}
    return {"role": "customer"}

# ==========================================
# 🛑 CORE API REST ROUTE ENDPOINTS
# ==========================================

# --- 1. AUTH SYSTEM ---
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Email is already in use"}), 409
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        user_id=generate_uuid(),
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        password_hash=hashed_password,
        user_role=data.get('role', 'customer')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!", "userId": new_user.user_id}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not bcrypt.check_password_hash(user.password_hash, data.get('password')):
        return jsonify({"error": "Invalid email or password parameters"}), 401
        
    access_token = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.user_role,
        "user_id": user.user_id
    }), 200

# --- 2. VEHICLE MANAGEMENT SYSTEM ---
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    v_type = request.args.get('type')
    query = Vehicle.query.filter_by(availability_status='available')
    
    if v_type:
        query = query.filter_by(vehicle_type=v_type)
        
    vehicles = query.all()
    output = []
    for v in vehicles:
        output.append({
            "vehicle_id": v.vehicle_id,
            "make": v.make,
            "model": v.model,
            "year": v.year,
            "type": v.vehicle_type,
            "rate_kes": float(v.daily_rental_rate)
        })
    return jsonify(output), 200

@app.route('/api/vehicles', methods=['POST'])
@role_required(['admin'])
def add_vehicle():
    data = request.get_json()
    new_car = Vehicle(
        vehicle_id=generate_uuid(),
        make=data['make'],
        model=data['model'],
        year=data['year'],
        vehicle_type=data['vehicle_type'],
        license_plate=data['license_plate'],
        vin=data['vin'],
        daily_rental_rate=data['daily_rental_rate']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Vehicle added successfully", "vehicle_id": new_car.vehicle_id}), 201

# --- 3. RENTAL BOOKINGS ---
@app.route('/api/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle or vehicle.availability_status != 'available':
        return jsonify({"error": "Vehicle is currently unavailable"}), 400
        
    start = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end = datetime.strptime(data['end_date'], '%Y-%m-%d')
    duration = (end - start).days
    
    if duration <= 0:
        return jsonify({"error": "Invalid date range structure"}), 400
        
    subtotal = duration * float(vehicle.daily_rental_rate)
    insurance = subtotal * 0.05 if data.get('include_insurance') else 0.0
    total = subtotal + insurance
    
    booking = Booking(
        booking_id=generate_uuid(),
        user_id=user_id,
        vehicle_id=vehicle.vehicle_id,
        booking_reference=generate_reference("BK"),
        start_date=start,
        end_date=end,
        rental_duration_days=duration,
        daily_rate=vehicle.daily_rental_rate,
        subtotal=subtotal,
        insurance_charge=insurance,
        total_amount=total,
        payment_method=data.get('payment_method', 'mpesa')
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking request initialized", "booking_reference": booking.booking_reference, "total_kes": total}), 201

# --- 4. SERVICE REQUESTS ---
@app.route('/api/service-requests', methods=['POST'])
@jwt_required()
def submit_service_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    p_date = datetime.strptime(data['preferred_date'], '%Y-%m-%d').date()
    p_time = datetime.strptime(data['preferred_time'], '%H:%M').time()
    
    new_request = ServiceRequest(
        request_id=generate_uuid(),
        user_id=user_id,
        request_reference=generate_reference("SR"),
        full_name=data['full_name'],
        phone_number=data['phone_number'],
        service_type=data['service_type'],
        vehicle_details=data['vehicle_details'],
        issue_description=data.get('issue_description'),
        preferred_date=p_date,
        preferred_time=p_time,
        estimated_cost=data.get('estimated_cost', 3000.00) # Baseline minimum diagnosis cost
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Service ticket generated", "reference": new_request.request_reference}), 201

# --- 5. KENYAN DARAJA M-PESA STK WEBHOOK STUB ---
@app.route('/api/payments/mpesa-callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    # Parsing body schemas securely from Safaricom Daraja API callbacks
    try:
        stk_callback = data['Body']['stkCallback']
        result_code = stk_callback['ResultCode']
        merchant_request_id = stk_callback['MerchantRequestID']
        
        if result_code == 0:
            meta_items = stk_callback['CallbackMetadata']['Item']
            mpesa_receipt = next(item['Value'] for item in meta_items if item['Name'] == 'MpesaReceiptNumber')
            
            # Match the dynamic response tracking transaction
            payment = Payment.query.filter_by(transaction_id=merchant_request_id).first()
            if payment:
                payment.payment_status = 'completed'
                payment.transaction_id = mpesa_receipt # Swap Request token ID out for original receipt code.
                
                if payment.booking_id:
                    b = Booking.query.get(payment.booking_id)
                    b.payment_status = 'completed'
                    b.booking_status = 'confirmed'
                db.session.commit()
                
        return jsonify({"ResultCode": 0, "ResultDesc": "Callback processed smoothly"}), 200
    except Exception as e:
        return jsonify({"ResultCode": 1, "ResultDesc": f"Fail verification parsing: {str(e)}"}), 400

# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)