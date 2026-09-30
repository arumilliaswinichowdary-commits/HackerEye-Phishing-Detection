from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import joblib
from feature_extraction import extract_features
import time


app = Flask(__name__)


# ---------------- DATABASE CONNECTION ----------------

import os

conn = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
)

cursor = conn.cursor(buffered=True)



# ---------------- LOAD AI MODEL ----------------

model = joblib.load("model.pkl")

print("Model expects:", model.n_features_in_)




# ---------------- HOME PAGE ----------------

@app.route('/')
def home():

    return render_template("index.html")




# ---------------- SCANNER PAGE ----------------

@app.route('/scanner')
def scanner():

    return render_template("scanner.html")





# ---------------- LOADING PAGE ----------------

@app.route('/loading')
def loading():

    url = request.args.get("url")

    return render_template(
        "loading.html",
        url=url
    )





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


    cursor.execute(
        sql,
        (username,email,password)
    )


    conn.commit()


    return redirect('/login')







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


    cursor.execute(
        sql,
        (username,password)
    )


    user = cursor.fetchall()



    if user:

        return redirect('/scanner')


    else:

        return "Invalid Username or Password"








# ---------------- AI SCANNER ----------------



from urllib.parse import urlparse

@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']

    parsed = urlparse(url)

    if not parsed.scheme or not parsed.netloc:
        return render_template(
            "result.html",
            url=url,
            result="Invalid URL",
            threat="UNKNOWN",
            confidence=0
        )

    return redirect(
        url_for(
            'loading',
            url=url
        )
    )







# ---------------- FINAL SCAN RESULT ----------------



@app.route('/result')
def result():


    url = request.args.get("url")



    # Feature extraction

    features = extract_features(url)



    prediction = model.predict([features])



    probability = model.predict_proba([features])



    confidence = round(
        max(probability[0])*100,
        2
    )




    if prediction[0] == 0:


        status = "Legitimate Website"


        threat = "LOW"


    else:


        status = "Phishing Website"


        threat = "HIGH"






    # Save Scan History


    sql = """
    INSERT INTO predictions(url,result)
    VALUES(%s,%s)
    """



    cursor.execute(
        sql,
        (url,status)
    )


    conn.commit()





    return render_template(

        "result.html",

        url=url,

        result=status,

        threat=threat,

        confidence=confidence

    )







# ---------------- DASHBOARD ----------------


@app.route('/dashboard')
def dashboard():


    cursor.execute(
        "SELECT * FROM predictions ORDER BY id DESC"
    )


    scans = cursor.fetchall()



    return render_template(

        "dashboard.html",

        scans=scans

    )







if __name__ == "__main__":

    app.run(debug=True)