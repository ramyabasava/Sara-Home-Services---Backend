from flask import Flask, jsonify, request, g
from flask_cors import CORS
import sqlite3
import bcrypt

from database import get_db_connection

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

DATABASE = 'serviceonwheel.db'

def get_db():
    """Get a database connection for the current request."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- API Endpoints ---

# Endpoint for User Registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    db = get_db()
    cursor = db.cursor()

    # Check if user already exists
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        return jsonify({'message': 'User with this email already exists'}), 409

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert new user
    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
    db.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Endpoint for User Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({
            'message': 'Login successful',
            'user': {'id': user['id'], 'email': user['email']}
        }), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# Endpoint to get all testimonials
@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM testimonials')
    testimonials = [dict(row) for row in cursor.fetchall()]
    return jsonify(testimonials)
    
# ... other imports

# Endpoint to get all services
@app.route('/api/services', methods=['GET']) #<-- 1. Defines the URL path
def get_services():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM services') #<-- 2. Gets data from the database
    services = [dict(row) for row in cursor.fetchall()]
    return jsonify(services) #<-- 3. Sends the data back as JSON
    
# Endpoint for the search functionality
@app.route('/api/search', methods=['GET'])
def search_services():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    db = get_db()
    cursor = db.cursor()
    search_term = f'%{query}%'
    cursor.execute(
        "SELECT * FROM services WHERE name LIKE ? OR description LIKE ?",
        (search_term, search_term)
    )
    services = [dict(row) for row in cursor.fetchall()]
    return jsonify(services)
 # Endpoint to get a single service by ID
@app.route('/api/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM services WHERE id = ?', (service_id,))
    service = cursor.fetchone()
    if service is None:
        return jsonify({'message': 'Service not found'}), 404
    return jsonify(dict(service))

# Endpoint to create a new booking
@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    # Get all fields from the request payload
    user_id = data.get('user_id')
    service_id = data.get('service_id')
    customer_name = data.get('customer_name')
    address = data.get('address')
    booking_date = data.get('booking_date')
    booking_time = data.get('booking_time')
    payment_method = data.get('payment_method')

    # CRITICAL: This validation check MUST include all required fields
    if not all([user_id, service_id, customer_name, address, booking_date, booking_time, payment_method]):
        # If this message shows up in your browser's Network tab, a field is missing
        return jsonify({'message': 'Missing required booking information'}), 400

    db = get_db()
    cursor = db.cursor()

    # Get service name from service_id
    cursor.execute('SELECT name FROM services WHERE id = ?', (service_id,))
    service = cursor.fetchone()
    if not service:
        return jsonify({'message': 'Invalid service ID'}), 400
    service_name = service['name']

    # CRITICAL: The INSERT statement MUST match the database schema exactly
    try:
        cursor.execute(
            'INSERT INTO bookings (user_id, service_id, service_name, customer_name, address, booking_date, booking_time, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (user_id, service_id, service_name, customer_name, address, booking_date, booking_time, payment_method)
        )
        booking_id = cursor.lastrowid
        db.commit()
    except Exception as e:
        # If the server crashes, this will help identify the error
        print(f"Database Error: {e}")
        return jsonify({'message': 'A database error occurred.'}), 500


    return jsonify({
        'message': 'Booking created successfully',
        'booking_id': booking_id,
        'booking_details': {
            'service_name': service_name,
            'customer_name': customer_name,
            'address': address,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'payment_method': payment_method
        }
    }), 201
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
