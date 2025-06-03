# Smart-sensor-for-Emotional-Harmony-

This project is an **Smart-sensor-for-Emotional-Harmony** that uses facial emotion detection to recommend music tailored to a user's current mood. Built with Python, OpenCV, Keras, and additional frontend technologies, the application captures a user's facial expression, determines the emotion, and plays music accordingly.


## Features

-   Real-time Emotion Detection using webcam
   -Mood-based music recommendation
  - User Authentication (Login & Sign Up)
-  Deep Learning model trained to detect multiple emotions
-  Music categorized based on emotion (e.g., Happy, Sad, Angry, Neutral)

##  Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Libraries/Frameworks:** OpenCV, Keras, TensorFlow, NumPy, Pandas
- **Authentication:** Flask sessions, secure user login/sign-up
- **Model:** CNN-based emotion detection
- **Dataset:** Pretrained model and images for training/testing

- ## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Smart-sensor-for-Emotional-Harmony.git
cd Smart-sensor-for-Emotional-Harmony
```

### 2. Create and Activate a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

If `requirements.txt` is not available, install the major packages:

```bash
pip install flask opencv-python tensorflow keras numpy pandas
```

### 4. Run the App

```bash
python app.py
```

Open your browser and navigate to:  
`http://127.0.0.1:5000`

## Project Structure

```
Emotion-Music-Recommendation/
├── static/
│   └── songs/               
├── templates/
│   ├── index.html         
│   ├── login.html           
│   ├── signup.html          
│   ├── dashboard.html      
├── model/
│   └── emotion_model.h5     
├── app.py                  
├── camera.py               
├── emotion_detector.py      
├── utils.py           
└── README.md
```

## Authentication Details

- Users must **sign up** and **log in** to access the dashboard and use the emotion-based recommendation system.
- Credentials are stored securely using hashed passwords (if implemented).

## How it Works

1. User logs in/signs up.
2. The app accesses the webcam and detects facial emotion.
3. Based on the detected emotion, a music playlist from the appropriate folder is played.

##  Emotions Detected

- Happy
- Sad
- Angry
- Neutral
- Surprise (if trained)
- Fear (if trained)
- Disgust (if trained)

## Future Improvements

- Spotify API integration
- Emotion detection from speech
- Enhanced UI/UX design
- User music history and preferences

