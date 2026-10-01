from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import joblib
import os
from urllib.parse import urlparse

from feature_extraction import extract_features


# --------------------------------------------------
# FLASK APP
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )


# --------------------------------------------------
# LOAD MACHINE LEARNING MODEL
# --------------------------------------------------

model = joblib.load("model_small.pkl")

print("Model expects:", model.n_features_in_)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# SCANNER PAGE
# --------------------------------------------------

@app.route("/scanner")
def scanner():
    return render_template("scanner.html")


# --------------------------------------------------
# LOADING PAGE
# --------------------------------------------------

@app.route("/loading")
def loading():
    return render_template("loading.html")


# --------------------------------------------------
# REGISTER PAGE
# --------------------------------------------------

@app.route("/register")
def register():
    return render_template("register.html")


# --------------------------------------------------
# REGISTER USER
# --------------------------------------------------

@app.route("/register", methods=["POST"])
def register_user():

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (username, email, password))

        conn.commit()

        return "Registration Successful!"

    except Exception as e:

        print("Registration Error:", e)

        return "Registration failed. Please try again."

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------

@app.route("/login")
def login():
    return render_template("login.html")


# --------------------------------------------------
# LOGIN USER
# --------------------------------------------------

@app.route("/login", methods=["POST"])
def login_user():

    username = request.form["username"]
    password = request.form["password"]

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(buffered=True)

        sql = """
        SELECT * FROM users
        WHERE username = %s AND password = %s
        """

        cursor.execute(sql, (username, password))

        user = cursor.fetchone()

        if user:

            return redirect(url_for("scanner"))

        else:

            return "Invalid Username or Password"

    except Exception as e:

        print("Login Error:", e)

        return "Login failed. Please try again."

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# --------------------------------------------------
# PREDICT / SCAN URL
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    url = request.form.get("url", "").strip()

    if not url:

        return "Please enter a URL."

    # Add https if user did not provide a protocol
    if not url.startswith(("http://", "https://")):

        url = "https://" + url

    # Basic URL validation
    try:

        parsed_url = urlparse(url)

        if not parsed_url.netloc:

            return "Invalid URL. Please enter a valid website URL."

    except Exception:

        return "Invalid URL."

    # Redirect to loading page
    return redirect(
        url_for("loading", url=url)
    )


# --------------------------------------------------
# RESULT PAGE
# --------------------------------------------------

@app.route("/result")
def result():

    url = request.args.get("url", "").strip()

    if not url:

        return redirect(url_for("scanner"))

    try:

        # Extract URL features
        features = extract_features(url)

        # Convert features into model input
        prediction = model.predict([features])[0]

        # Get confidence if available
        confidence = None

        try:

            probabilities = model.predict_proba([features])[0]

            confidence = round(
                max(probabilities) * 100,
                2
            )

        except Exception:

            confidence = None

        # ------------------------------------------
        # DETERMINE RESULT
        # ------------------------------------------

        if prediction == 1:

            status = "Malicious Website"

        else:

            status = "Legitimate Website"

        # ------------------------------------------
        # SAVE SCAN RESULT TO DATABASE
        # ------------------------------------------

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            sql = """
            INSERT INTO predictions (url, result)
            VALUES (%s, %s)
            """

            cursor.execute(
                sql,
                (url, status)
            )

            conn.commit()

            cursor.close()
            conn.close()

        except Exception as db_error:

            print(
                "Database Error:",
                db_error
            )

        # ------------------------------------------
        # SHOW RESULT
        # ------------------------------------------

        return render_template(
            "dashboard.html",
            url=url,
            status=status,
            confidence=confidence
        )

    except Exception as e:

        print(
            "Prediction Error:",
            e
        )

        return "Error while scanning the website."


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    conn = None
    cursor = None

    try:

        conn = get_db_connection()

        cursor = conn.cursor(
            buffered=True
        )

        cursor.execute(
            "SELECT * FROM predictions ORDER BY id DESC"
        )

        scans = cursor.fetchall()

        return render_template(
            "dashboard.html",
            scans=scans
        )

    except Exception as e:

        print(
            "Dashboard Error:",
            e
        )

        return render_template(
            "dashboard.html",
            scans=[]
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# --------------------------------------------------
# RUN FLASK APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )