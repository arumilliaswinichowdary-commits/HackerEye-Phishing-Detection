from flask import Flask, render_template, request
import mysql.connector
import joblib
from feature_extraction import extract_features
app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhara@123",
    database="hackereye"
)

cursor = conn.cursor(buffered=True)
model = joblib.load("model.pkl")
print("Model expects:", model.n_features_in_)
@app.route('/')
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_user():

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    sql = """
    INSERT INTO users(username,email,password)
    VALUES(%s,%s,%s)
    """

    values = (username, email, password)

    cursor.execute(sql, values)

    conn.commit()

    return "Registration Successful!"


# ---------------- LOGIN ----------------

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_user():

    username = request.form['username']
    password = request.form['password']

    sql = """
    SELECT * FROM users
    WHERE username=%s AND password=%s
    """

    values = (username, password)

    cursor.execute(sql, values)

    user = cursor.fetchall()

    if user:
        return render_template("index.html")
    else:
        return "Invalid Username or Password"


# ---------------- PREDICTION ----------------

@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']

    features = extract_features(url)

    prediction = model.predict([features])

    if prediction[0] == 0:
        result = "Legitimate Website"
    else:
        result = "Phishing Website"

    sql = """
    INSERT INTO predictions(url,result)
    VALUES(%s,%s)
    """

    values = (url, result)

    cursor.execute(sql, values)

    conn.commit()

    return render_template(
        "result.html",
        result=result
    )


if __name__ == '__main__':
    app.run(debug=True)