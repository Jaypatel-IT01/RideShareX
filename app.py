from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection
import os

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-secret-key"
)

# Used for login sessions
#app.secret_key = "ridesharex-secret-key"


# =========================
# HOME PAGE
# =========================

@app.route("/")
def index():

    return render_template("index.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        user_type = request.form["user_type"]

        password = request.form["password"]
        confirm_password = request.form["confirm_password"]


        # Check passwords

        if password != confirm_password:

            return "Passwords do not match!"


        # Hash password

        hashed_password = generate_password_hash(password)


        connection = get_connection()

        cursor = connection.cursor()


        query = """
        INSERT INTO users
        (name, email, phone, user_type, password)
        VALUES (%s, %s, %s, %s, %s)
        """


        values = (
            name,
            email,
            phone,
            user_type,
            hashed_password
        )


        try:

            cursor.execute(query, values)

            connection.commit()

            return redirect(url_for("login"))


        except Exception as e:

            connection.rollback()

            return f"Registration failed: {e}"


        finally:

            cursor.close()

            connection.close()


    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        connection = get_connection()

        cursor = connection.cursor(dictionary=True)


        query = """
        SELECT *
        FROM users
        WHERE email = %s
        """


        cursor.execute(query, (email,))


        user = cursor.fetchone()


        cursor.close()

        connection.close()


        # User not found

        if user is None:

            return "Invalid email or password!"


        # Check password

        if not check_password_hash(
            user["password"],
            password
        ):

            return "Invalid email or password!"


        # Create session

        session["user_id"] = user["id"]

        session["user_name"] = user["name"]

        session["user_email"] = user["email"]

        session["user_type"] = user["user_type"]


        # Redirect to dashboard

        return redirect(
            url_for("dashboard")
        )


    return render_template("login.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    # Check if user is logged in

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "dashboard.html",
        user_name=session["user_name"],
        user_type=session["user_type"]
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )

# =========================
# FIND RIDE
# =========================

@app.route("/find-ride")
def find_ride():

    # User must be logged in

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "find_ride.html"
    )

# =========================
# OFFER A RIDE
# =========================

@app.route("/offer-ride", methods=["GET", "POST"])
def offer_ride():

    # User must be logged in

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    if request.method == "POST":

        from_location = request.form["from_location"]

        to_location = request.form["to_location"]

        travel_date = request.form["travel_date"]

        travel_time = request.form["travel_time"]

        available_seats = request.form["available_seats"]

        price = request.form["price"]

        vehicle_details = request.form["vehicle_details"]


        # Get logged-in user

        driver_id = session["user_id"]


        # Connect database

        connection = get_connection()

        cursor = connection.cursor()


        query = """
        INSERT INTO rides
        (
            driver_id,
            from_location,
            to_location,
            travel_date,
            travel_time,
            available_seats,
            price,
            vehicle_details
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """


        values = (
            driver_id,
            from_location,
            to_location,
            travel_date,
            travel_time,
            available_seats,
            price,
            vehicle_details
        )


        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()


            return """
            <h1>Ride Published Successfully! 🚗</h1>

            <p>
            Your ride is now available for passengers.
            </p>

            <a href="/dashboard">
                Go to Dashboard
            </a>
            """


        except Exception as e:

            connection.rollback()

            return f"Failed to publish ride: {e}"


        finally:

            cursor.close()

            connection.close()


    return render_template(
        "offer_ride.html"
    )
    
# =========================
# SEARCH RIDES
# =========================

@app.route("/search-rides")
def search_rides():

    if "user_id" not in session:
        return redirect(url_for("login"))

    from_location = request.args.get(
        "from_location",
        ""
    ).strip()

    to_location = request.args.get(
        "to_location",
        ""
    ).strip()

    travel_date = request.args.get(
        "travel_date",
        ""
    ).strip()


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # Get all available rides
    # on the selected date

    cursor.execute(
        """
        SELECT
            rides.*,
            users.name

        FROM rides

        JOIN users
        ON rides.driver_id = users.id

        WHERE rides.travel_date = %s

        AND rides.available_seats > 0

        AND rides.driver_id != %s

        """,
        (
            travel_date,
            session["user_id"]
        )
    )


    all_rides = cursor.fetchall()


    cursor.close()

    connection.close()



    # =========================
    # LOCATION MATCHING
    # =========================

    search_from = from_location.lower()

    search_to = to_location.lower()


    rides = []


    for ride in all_rides:

        ride_from = (
            ride["from_location"]
            .lower()
        )

        ride_to = (
            ride["to_location"]
            .lower()
        )


        # Exact match

        if (
            ride_from == search_from
            and
            ride_to == search_to
        ):

            ride["match_type"] = "Exact Match"

            ride["match_score"] = 100

            rides.append(ride)


        # Same starting location

        elif ride_from == search_from:

            ride["match_type"] = "Same Starting Location"

            ride["match_score"] = 70

            rides.append(ride)


        # Same destination

        elif ride_to == search_to:

            ride["match_type"] = "Same Destination"

            ride["match_score"] = 60

            rides.append(ride)


    # Sort highest match first

    rides.sort(
        key=lambda x:
            x["match_score"],
        reverse=True
    )


    return render_template(

        "search_results.html",

        rides=rides,

        from_location=from_location,

        to_location=to_location,

        travel_date=travel_date

    )
# =========================
# RIDE DETAILS
# =========================

@app.route("/ride/<int:ride_id>")
def ride_details(ride_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # =========================
    # GET RIDE
    # =========================

    cursor.execute(
        """
        SELECT
            rides.*,
            users.name

        FROM rides

        JOIN users
        ON rides.driver_id = users.id

        WHERE rides.id = %s
        """,
        (ride_id,)
    )


    ride = cursor.fetchone()


    if ride is None:

        cursor.close()

        connection.close()

        return "Ride not found!", 404



    # =========================
    # GET PASSENGERS
    # =========================

    cursor.execute(
        """
        SELECT

            users.id,

            users.name,

            users.email,

            users.phone,

            bookings.seats_booked,

            bookings.booking_status

        FROM bookings

        JOIN users

        ON bookings.passenger_id = users.id

        WHERE bookings.ride_id = %s

        AND bookings.booking_status = 'confirmed'

        ORDER BY bookings.created_at ASC

        """,
        (ride_id,)
    )


    passengers = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "ride_details.html",

        ride=ride,

        passengers=passengers

    )
# =========================
# JOIN RIDE
# =========================

@app.route("/my-rides")
def my_rides():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # =========================
    # RIDES OFFERED BY USER
    # =========================

    cursor.execute(
        """
        SELECT *
        FROM rides
        WHERE driver_id = %s
        ORDER BY travel_date ASC
        """,
        (user_id,)
    )


    offered_rides = cursor.fetchall()



    # =========================
    # RIDES JOINED BY USER
    # =========================

    cursor.execute(
        """
        SELECT

            rides.*,

            users.name AS driver_name,

            bookings.seats_booked,

            bookings.booking_status

        FROM bookings

        JOIN rides
        ON bookings.ride_id = rides.id

        JOIN users
        ON rides.driver_id = users.id

        WHERE bookings.passenger_id = %s

        ORDER BY rides.travel_date ASC
        """,
        (user_id,)
    )


    joined_rides = cursor.fetchall()



    cursor.close()

    connection.close()



    return render_template(

        "my_rides.html",

        offered_rides=offered_rides,

        joined_rides=joined_rides

    )
    
@app.route(
    "/cancel-booking/<int:ride_id>",
    methods=["POST"]
)
def cancel_booking(ride_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        # Find the user's booking

        cursor.execute(
            """
            SELECT
                id,
                seats_booked

            FROM bookings

            WHERE ride_id = %s

            AND passenger_id = %s

            AND booking_status = 'confirmed'
            """,
            (
                ride_id,
                user_id
            )
        )


        booking = cursor.fetchone()


        if booking is None:

            connection.rollback()

            return "Booking not found!", 404


        seats_booked = booking["seats_booked"]


        # Cancel booking

        cursor.execute(
            """
            UPDATE bookings

            SET booking_status = 'cancelled'

            WHERE id = %s
            """,
            (
                booking["id"],
            )
        )


        # Return seats to ride

        cursor.execute(
            """
            UPDATE rides

            SET available_seats =
                available_seats + %s

            WHERE id = %s
            """,
            (
                seats_booked,
                ride_id
            )
        )


        connection.commit()


        return redirect(
            url_for("my_rides")
        )


    except Exception as e:

        connection.rollback()

        return f"Unable to cancel booking: {e}"


    finally:

        cursor.close()

        connection.close()
        
@app.route(
    "/cancel-ride/<int:ride_id>",
    methods=["POST"]
)
def cancel_ride(ride_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    connection = get_connection()

    cursor = connection.cursor()


    try:

        # Make sure the ride belongs
        # to the logged-in driver

        cursor.execute(
            """
            SELECT id

            FROM rides

            WHERE id = %s

            AND driver_id = %s
            """,
            (
                ride_id,
                user_id
            )
        )


        ride = cursor.fetchone()


        if ride is None:

            connection.rollback()

            return "Ride not found!", 404


        # Cancel all active bookings

        cursor.execute(
            """
            UPDATE bookings

            SET booking_status = 'cancelled'

            WHERE ride_id = %s

            AND booking_status = 'confirmed'
            """,
            (
                ride_id,
            )
        )


        # Delete the ride

        cursor.execute(
            """
            DELETE FROM rides

            WHERE id = %s

            AND driver_id = %s
            """,
            (
                ride_id,
                user_id
            )
        )


        connection.commit()


        return redirect(
            url_for("my_rides")
        )


    except Exception as e:

        connection.rollback()

        return f"Unable to cancel ride: {e}"


    finally:

        cursor.close()

        connection.close()     
        
# =========================
# MY PROFILE
# =========================

@app.route(
    "/profile",
    methods=["GET", "POST"]
)
def profile():

    # User must be logged in

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # =========================
    # UPDATE PROFILE
    # =========================

    if request.method == "POST":

        name = request.form["name"].strip()

        email = request.form["email"].strip()

        phone = request.form["phone"].strip()


        # Basic validation

        if not name or not email:

            cursor.close()

            connection.close()

            return "Name and email are required!"


        try:

            cursor.execute(
                """
                UPDATE users

                SET
                    name = %s,
                    email = %s,
                    phone = %s

                WHERE id = %s
                """,
                (
                    name,
                    email,
                    phone,
                    user_id
                )
            )


            connection.commit()


            # Update session name

            session["user_name"] = name


        except Exception as e:

            connection.rollback()

            cursor.close()

            connection.close()

            return f"Unable to update profile: {e}"



    # =========================
    # GET USER DATA
    # =========================

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            phone

        FROM users

        WHERE id = %s
        """,
        (user_id,)
    )


    user = cursor.fetchone()


    cursor.close()

    connection.close()


    if user is None:

        return "User not found!", 404


    return render_template(

        "profile.html",

        user=user

    )  
    
@app.route(
    "/join-ride/<int:ride_id>",
    methods=["POST"]
)
def join_ride(ride_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    passenger_id = session["user_id"]


    seats = int(
        request.form.get(
            "seats",
            1
        )
    )


    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        # =========================
        # GET RIDE
        # =========================

        cursor.execute(
            """
            SELECT *

            FROM rides

            WHERE id = %s

            FOR UPDATE
            """,
            (ride_id,)
        )


        ride = cursor.fetchone()


        if ride is None:

            return "Ride not found!", 404



        # =========================
        # DRIVER CANNOT JOIN
        # =========================

        if ride["driver_id"] == passenger_id:

            return "You cannot join your own ride!"



        # =========================
        # CHECK SEATS
        # =========================

        if seats <= 0:

            return "Invalid number of seats!"



        if ride["available_seats"] < seats:

            return "Not enough seats available!"

        # =========================
        # CHECK DUPLICATE BOOKING
        # =========================

        cursor.execute(
            """
            SELECT id
            FROM bookings
            WHERE ride_id = %s
            AND passenger_id = %s
            AND booking_status = 'confirmed'
            """,
            (ride_id, passenger_id)
        )

        existing_booking = cursor.fetchone()

        if existing_booking:

            return "You have already joined this ride!"

        # =========================
        # CREATE BOOKING
        # =========================

        cursor.execute(
            """
            INSERT INTO bookings

            (
                ride_id,
                passenger_id,
                seats_booked,
                booking_status
            )

            VALUES
            (
                %s,
                %s,
                %s,
                'confirmed'
            )
            """,
            (
                ride_id,
                passenger_id,
                seats
            )
        )


        # =========================
        # UPDATE SEATS
        # =========================

        cursor.execute(
            """
            UPDATE rides

            SET available_seats =
                available_seats - %s

            WHERE id = %s
            """,
            (
                seats,
                ride_id
            )
        )


        connection.commit()


        return redirect(
            url_for(
                "ride_details",
                ride_id=ride_id
            )
        )


    except Exception as e:

        connection.rollback()

        return f"Unable to join ride: {e}"


    finally:

        cursor.close()

        connection.close()                          

# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(debug=True)