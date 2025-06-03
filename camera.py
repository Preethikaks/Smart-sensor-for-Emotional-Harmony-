import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import pandas as pd

# Load Haarcascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load Emotion Detection Model
emotion_model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])
emotion_model.load_weights('model.h5')

# Emotion categories
emotion_dict = {
    0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy",
    4: "Neutral", 5: "Sad", 6: "Surprised"
}

# Alert messages
emotion_alerts = {
    "Angry": "Take a deep breath! Let’s cool down with some soothing tunes.",
    "Disgusted": "Something’s not right? Maybe a change in mood with music will help!",
    "Fearful": "Feeling uneasy? Music can be your comfort. Stay calm and listen to this playlist.",
    "Happy": "You look happy! Keep smiling and enjoy some uplifting music!",
    "Neutral": "Feeling neutral? Here’s something to match your vibe or lift your mood!",
    "Sad": "Why the sad face? Here's some music to lift your spirits. Stay strong!",
    "Surprised": "Wow! Something caught you off guard? Let’s find the perfect track to match this moment."
}
music_dist = {
    "Angry": "songs/angry.csv",
    "Disgusted": "songs/disgusted.csv",
    "Fearful": "songs/fearful.csv",
    "Happy": "songs/happy.csv",
    "Neutral": "songs/neutral.csv",
    "Sad": "songs/sad.csv",
    "Surprised": "songs/surprised.csv"
}


class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        ret, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        detected_emotion = "Neutral"
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            detected_emotion = emotion_dict[maxindex]

            # Draw rectangle around face and label detected emotion
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 2)
            cv2.putText(frame, detected_emotion, (x+5, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Convert frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), detected_emotion, emotion_alerts[detected_emotion]
def music_rec(emotion):
    # Ensure music_dist contains paths to the correct CSV files
    try:
        df = pd.read_csv(music_dist[emotion])  # Assuming music_dist is a dictionary of emotion-to-CSV mappings
        return df.head(10).to_dict(orient='records')  # Return the top 10 songs as a dictionary
    except FileNotFoundError:
        # If the file for the given emotion doesn't exist, return a placeholder message
        return [{"Name": "No songs found", "Album": "N/A", "Artist": "N/A"}]
