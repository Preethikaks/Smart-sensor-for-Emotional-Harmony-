from flask import Flask, render_template, Response, jsonify, request, redirect, session
import mysql.connector
import bcrypt  # ✅ Added for password hashing
import pandas as pd
from camera import VideoCamera

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# ✅ Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="7019838679",
        database="emotion_music_db"
    )

# ✅ Emotion-based music data
music_dist = {
    "Angry": "songs/angry.csv",
    "Disgusted": "songs/disgusted.csv",
    "Fearful": "songs/fearful.csv",
    "Happy": "songs/happy.csv",
    "Neutral": "songs/neutral.csv",
    "Sad": "songs/sad.csv",
    "Surprised": "songs/surprised.csv"
}

# ✅ Function to fetch songs based on detected emotion
def music_rec(emotion):
    file_path = music_dist.get(emotion, "songs/neutral.csv")  # Default to neutral
    df = pd.read_csv(file_path)
    return df[['Name', 'Album', 'Artist']].head(15).to_dict(orient='records')

# ✅ Home Route (Redirects to login if not logged in)
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')

# ✅ Video Feed Route
def gen(camera):
    while True:
        frame, detected_emotion, alert_message = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ✅ Detect Emotion Route
@app.route('/detect_emotion')
def detect_emotion():
    camera = VideoCamera()
    _, detected_emotion, alert_message = camera.get_frame()
    return jsonify({'emotion': detected_emotion, 'alert': alert_message})

# ✅ Recommendations Page (Based on Emotion)
@app.route('/recommendations/<emotion>')
def recommendations_with_emotion(emotion):
    if 'user_id' not in session:
        return redirect('/login')
    songs = music_rec(emotion)
    return render_template('recommendations.html', songs=songs, emotion=emotion)

# ✅ Login Route (Now Uses Hashed Passwords)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        db.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):  # Verify password
            session['user_id'] = user[0]  # Store user ID in session
            return redirect('/')
        else:
            return '''<script>alert("Invalid email or password!"); window.location.href="/login";</script>'''  # ✅ Show JavaScript Alert
    return render_template('login.html')

# ✅ Signup Route (Now Hashes Passwords)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, hashed_password.decode('utf-8')))
        db.commit()
        db.close()

        return redirect('/login')

    return render_template('signup.html')

# ✅ Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
