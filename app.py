from flask import Flask, request, jsonify, render_template, redirect
import pandas as pd
import os
import csv
import hashlib
import random

app = Flask(__name__)

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_FILE = os.path.join(
    BASE_DIR,
    'song_dataset_clustered.csv'
)

USERS_FILE = os.path.join(
    BASE_DIR,
    'users.csv'
)

# =========================
# LOAD DATASET
# =========================
try:

    songs_df = pd.read_csv(DATASET_FILE)

    songs_df.fillna('', inplace=True)

    SONGS_DATA = []

    for index, row in songs_df.iterrows():

        SONGS_DATA.append({

            "id": int(index),

            "name": str(row.get("name", "")),

            "artist": str(row.get("artist", "")),

            "genre": str(row.get("genre", "Music")),

            "cover": "default.png"
        })

    print("✅ Dataset Loaded Successfully")

except Exception as e:

    print("❌ Dataset Load Error:", e)

    SONGS_DATA = []

    songs_df = pd.DataFrame()


# =========================
# HOME
# =========================
@app.route('/')
def home():

    return redirect('/signup')


# =========================
# SIGNUP PAGE
# =========================
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':

        return render_template('signup.html')

    try:

        data = request.get_json(force=True)

        name = data.get('name')

        email = data.get('email')

        password = data.get('password')

        if not name or not email or not password:

            return jsonify({

                "success": False,

                "message": "All fields required"

            }), 400

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        # CREATE FILE IF NOT EXISTS
        if not os.path.exists(USERS_FILE):

            with open(
                USERS_FILE,
                'w',
                newline='',
                encoding='utf-8'
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    'name',
                    'email',
                    'password'
                ])

        # CHECK DUPLICATE EMAIL
        with open(
            USERS_FILE,
            'r',
            encoding='utf-8'
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) > 1 and row[1] == email:

                    return jsonify({

                        "success": False,

                        "message": "Email already exists"

                    })

        # SAVE USER
        with open(
            USERS_FILE,
            'a',
            newline='',
            encoding='utf-8'
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                name,
                email,
                hashed_password
            ])

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("Signup Error:", e)

        return jsonify({

            "success": False,

            "message": "Server Error"

        }), 500


# =========================
# LOGIN PAGE
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('login.html')

    try:

        data = request.get_json(force=True)

        email = data.get('email')

        password = data.get('password')

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        if not os.path.exists(USERS_FILE):

            return jsonify({

                "success": False,

                "message": "No users found"

            })

        with open(
            USERS_FILE,
            'r',
            encoding='utf-8'
        ) as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                if (
                    row[1] == email
                    and row[2] == hashed_password
                ):

                    return jsonify({

                        "success": True,

                        "name": row[0]

                    })

        return jsonify({

            "success": False,

            "message": "Invalid credentials"

        })

    except Exception as e:

        print("Login Error:", e)

        return jsonify({

            "success": False,

            "message": "Server Error"

        }), 500


# =========================
# PAGES
# =========================
@app.route('/select-songs')
def select_songs():

    return render_template('onboarding.html')


@app.route('/recommendations')
def recommendations():

    return render_template('recommendations.html')


@app.route('/main')
def main():

    return render_template('final.html')


# =========================
# SONG API
# =========================
@app.route('/api/songs', methods=['GET'])
def get_songs():

    try:

        query = request.args.get(
            'q',
            ''
        ).lower()

        filtered = SONGS_DATA

        if query:

            filtered = [

                song for song in SONGS_DATA

                if (
                    query in song['name'].lower()
                    or query in song['artist'].lower()
                    or query in song['genre'].lower()
                )
            ]

        return jsonify({

            "songs": filtered

        })

    except Exception as e:

        print("Song API Error:", e)

        return jsonify({
            "songs": []
        })


# =========================
# RANDOM RECOMMENDATIONS API
# =========================
@app.route('/api/random-recommendations')
def random_recommendations():

    try:

        recommendations = random.sample(

            SONGS_DATA,

            min(15, len(SONGS_DATA))
        )

        return jsonify({

            "recommendations": recommendations

        })

    except Exception as e:

        print("Recommendation Error:", e)

        return jsonify({
            "recommendations": []
        })


# =========================
# RUN SERVER
# =========================
if __name__ == '__main__':

    app.run(
        debug=True,
        port=5000
    )