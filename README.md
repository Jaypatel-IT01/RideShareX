# 🚗 RideShareX

> A web-based ride-sharing and carpooling platform that connects drivers and passengers traveling along similar routes, helping users share journeys and reduce travel costs.

---

## 📌 About the Project

**RideShareX** is a full-stack web application designed to make daily transportation more convenient, affordable, and efficient.

The platform allows users to:

- Create an account
- Log in securely
- Offer rides as a driver
- Search for available rides
- Find rides based on source, destination, and travel date
- View ride matching results
- Join available rides
- Book one or more seats
- View ride and driver information
- View passengers who joined a ride
- Cancel a booking
- Cancel an offered ride
- Manage personal profile information
- View offered and joined rides

RideShareX uses **Flask** as the backend framework, **MySQL** for database management, and **HTML, CSS, and JavaScript** for the frontend.

---

## 🎯 Project Objectives

The main objectives of RideShareX are:

1. To provide an easy-to-use platform for ride sharing.
2. To connect passengers with drivers traveling on similar routes.
3. To help users reduce transportation costs.
4. To make better use of empty seats in private vehicles.
5. To provide a simple ride search and matching system.
6. To manage ride bookings efficiently.
7. To provide users with control over their rides and bookings.
8. To demonstrate full-stack web development using Python and Flask.

---

## ✨ Features

### 👤 User Registration

Users can create an account by providing:

- Name
- Email
- Phone number
- User type
- Password
- Confirm password

Passwords are securely hashed before being stored in the database.

---

### 🔐 User Login

Registered users can log in using:

- Email
- Password

The application verifies the user's credentials and creates a session after successful login.

---

### 🏠 User Dashboard

After logging in, users are redirected to their dashboard.

The dashboard provides access to:

- Find a Ride
- Offer a Ride
- My Rides
- My Profile
- Logout

---

### 🔍 Find a Ride

Users can search for available rides using:

- Starting location
- Destination
- Travel date

The application searches available rides and displays suitable matches.

---

### 🤝 Ride Matching

RideShareX provides a basic ride matching system.

The system compares the passenger's requested route with available rides.

Matching categories include:

#### 🟢 Exact Match

The starting location and destination both match.

**Match Score: 100**

#### 🟡 Same Starting Location

The starting location matches.

**Match Score: 70**

#### 🔵 Same Destination

The destination matches.

**Match Score: 60**

Search results are sorted according to the highest match score.

---

### 🚗 Offer a Ride

Users can publish a ride by providing:

- Starting location
- Destination
- Travel date
- Travel time
- Available seats
- Price
- Vehicle details

The ride is associated with the logged-in user's account.

The user becomes the driver of the ride.

---

### 🪑 Join a Ride

Passengers can join available rides.

Users can select the number of seats they want to book.

The system checks:

- Whether the ride exists
- Whether the user is the driver
- Whether the requested number of seats is valid
- Whether enough seats are available

After successful booking:

- A booking record is created.
- The number of available seats is reduced.

---

### 📋 Ride Details

Users can view detailed information about a ride.

Ride information includes:

- Driver
- Starting location
- Destination
- Travel date
- Travel time
- Available seats
- Price
- Vehicle details

Confirmed passengers can also be displayed with information such as:

- Passenger name
- Email
- Phone
- Seats booked
- Booking status

---

### 🛣️ My Rides

Users can view two categories of rides:

#### Rides Offered

Rides created by the logged-in user as a driver.

#### Rides Joined

Rides where the logged-in user has joined as a passenger.

---

### ❌ Cancel Booking

Passengers can cancel their confirmed booking.

When a booking is cancelled:

- The booking status is changed to `cancelled`.
- The previously booked seats are returned to the ride.

---

### 🚫 Cancel Ride

Drivers can cancel rides they created.

When a ride is cancelled:

- Active bookings associated with the ride are cancelled.
- The ride is removed from the database.

---

### 👤 User Profile

Users can view and update their profile information.

Profile details include:

- Name
- Email
- Phone number

---

### 🔒 Session Management

RideShareX uses Flask sessions to manage logged-in users.

The application stores information such as:

- User ID
- User name
- User email
- User type

Users who are not logged in are redirected to the login page when accessing protected features.

---

## 🛠️ Technologies Used

### Backend

- Python
- Flask
- Werkzeug Security
- MySQL Connector

### Frontend

- HTML5
- CSS3
- JavaScript

### Database

- MySQL

### Development Tools

- Visual Studio Code
- MySQL 8.0
- MySQL Command Line Client
- Python 3.14

---

## 🏗️ Project Architecture

The project follows a simple Flask-based web application architecture.

```text
User
 │
 ▼
Frontend (HTML / CSS / JavaScript)
 │
 ▼
Flask Application
 │
 ├── Authentication
 │
 ├── User Management
 │
 ├── Ride Management
 │
 ├── Ride Search & Matching
 │
 ├── Booking Management
 │
 └── Profile Management
 │
 ▼
MySQL Database
