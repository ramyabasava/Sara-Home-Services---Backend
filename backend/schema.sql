-- Drop tables if they exist to ensure a clean slate
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS testimonials;
DROP TABLE IF EXISTS bookings;

-- User table for authentication
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Services table to store service information
CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    icon_name TEXT NOT NULL -- We'll use this to map to a React icon
);

-- Testimonials table
CREATE TABLE testimonials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT NOT NULL,
    author_name TEXT NOT NULL,
    author_title TEXT NOT NULL,
    author_avatar TEXT -- Path or identifier for the avatar image
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, -- Add user_id to link booking to a user
    service_id INTEGER NOT NULL,
    service_name TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    address TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    booking_time TEXT NOT NULL,
    payment_method TEXT NOT NULL, -- NEW: To store 'UPI' or 'Cash on Delivery'
    status TEXT NOT NULL DEFAULT 'Confirmed',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (service_id) REFERENCES services (id)
);

-- Pre-populate services table with data from the screenshot
INSERT INTO services (name, description, icon_name) VALUES
('AC Repair', 'Expert AC repair, installation, and maintenance services.', 'BsSun'),
('Plumbing', 'All kinds of plumbing work, from leaks to installations.', 'BsWrench'),
('Electrician', 'Safe and reliable electrical services for your home.', 'BsLightningFill'),
('Painting', 'Professional interior and exterior painting services.', 'BsBrush'),
('Appliance Repair', 'Repair for all major home appliances.', 'BsDisplay'),
('CCTV Camera', 'Installation and maintenance of security cameras.', 'BsCameraVideo'),
('Packers & Movers', 'Hassle-free moving and packing services.', 'BsBoxSeam');

-- Pre-populate testimonials table with data
INSERT INTO testimonials (quote, author_name, author_title, author_avatar) VALUES
('The electrician was punctual, professional, and fixed the issue in no time. I was very impressed with the quality of service. Highly recommend ServiceOnWheel!', 'Sarah L.', 'Homeowner', 'avatar1'),
('My AC broke down during a heatwave. I booked a service, and the technician arrived within 2 hours. Absolutely life-saving service!', 'Mike R.', 'Apartment Renter', 'avatar2'),
('Used their plumbing service for my cafe. The response was quick, and the problem was solved efficiently. The pricing was transparent and fair.', 'Priya K.', 'Small Business Owner', 'avatar3');