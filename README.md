# 🎵 Melody AI - Music Recommendation System

Melody AI is a full-stack AI-powered music recommendation web application that helps users discover songs based on their musical preferences. Users can create an account, select their favorite songs, and receive personalized recommendations through an intelligent recommendation engine.

The system uses **K-Means Clustering** to group similar songs and **Cosine Similarity** to find the most relevant recommendations based on audio features. Flask acts as the backend, connecting the frontend with the recommendation engine through REST APIs.

---

## 🚀 Features

- 🔐 Secure User Authentication (Signup & Login)
- 🎵 Personalized Music Recommendations
- 🤖 Recommendation Engine using K-Means Clustering & Cosine Similarity
- 🔍 Dynamic Song Search
- ⚡ REST API Integration using Flask
- 🎨 Responsive Spotify-inspired User Interface
- 📊 Large English & Hindi Music Dataset
- 🔄 Real-time Recommendation Generation

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- K-Means Clustering
- Cosine Similarity
- Pandas
- NumPy
- Joblib

### Data Storage
- CSV Dataset

---

## 📂 Project Structure

```text
Melody-AI/
│── static/
│   ├── css/
│   ├── js/
│   └── images/
│
│── templates/
│   ├── signup.html
│   ├── login.html
│   ├── onboarding.html
│   ├── recommendations.html
│   └── final.html
│
│── app.py
│── recommender.py
│── optimised_model.joblib
│── scaler.joblib
│── song_dataset.csv
│── song_dataset_clustered.csv
│── users.csv
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Melody-AI.git
```

### 2. Navigate to the project folder

```bash
cd Melody-AI
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in your browser

```
http://127.0.0.1:5000
```

---

## 🧠 How It Works

1. User creates an account or logs in.
2. Selects favorite songs from the available dataset.
3. Flask sends the selected song to the recommendation engine.
4. The recommendation engine identifies the song's cluster using **K-Means**.
5. **Cosine Similarity** is applied to find the most similar songs within that cluster.
6. The recommended songs are returned to the frontend and displayed instantly.

---

## 📸 Screenshots

Add screenshots of:
- Signup Page
- Login Page
- Song Selection
- Recommendations Page
- Final Recommendation Page

---

## 📈 Future Improvements

- Spotify API Integration
- Mood-Based Recommendations
- Playlist Generation
- User Listening History
- Collaborative Filtering
- Deep Learning Recommendation Models

---

## 👨‍💻 Author

**Rishit Negi**

- GitHub: https://github.com/Rishit205
- LinkedIn: *(www.linkedin.com/in/rishit-negi-228a35233)*

---

## 📄 License

This project is developed for educational and learning purposes.
