# Addict Aware

> AI-powered digital wellness platform that predicts addiction levels and analyzes emotional patterns using Machine Learning and Natural Language Processing.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-47A248?style=flat-square&logo=mongodb&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

---

## 🚀 Features

### 🤖 AI & Machine Learning Core
- **Predictive Engine (~93.8% Accuracy)** — Features a custom-trained **Random Forest Classifier** that evaluates real-world screen time data (hours spent, phone pickups, social media usage) to predict digital addiction levels (Low, Medium, High) with high precision.
- **Context-Aware Sentiment Analysis** — Utilizes **OpenAI's GPT-3.5-turbo** NLP engine to deeply analyze qualitative emotional user feedback, uncovering hidden sentiment patterns and correlating them with digital behaviors.

### User Module
- **User Registration & Login** — JWT-based authentication with bcrypt password hashing
- **Addiction Assessment** — Seamlessly log your digital habits and emotional state
- **Progress Tracking** — Interactive Chart.js visualizations of your ongoing journey
- **PDF Reports** — Downloadable progress reports dynamically generated with ReportLab
- **Health Tips** — Personalized behavioral recommendations based on model predictions
- **Feedback System** — Submit platform feedback with star ratings

### Admin Module
- **Admin Dashboard** — KPI cards, doughnut charts, recent assessment tables
- **User Management** — View, monitor, and delete users
- **Content Manager** — Add, edit, and delete awareness health tips
- **ML Control Panel** — View model performance, feature importance, trigger retraining
- **Feedback Review** — Monitor user feedback with sentiment analysis

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.9+, Flask 3.0 |
| Database | MongoDB (PyMongo) |
| ML Model | Random Forest (scikit-learn) |
| NLP | OpenAI GPT-3.5-turbo |
| Frontend | HTML5, CSS3, Bootstrap 5 (custom themed) |
| Charts | Chart.js |
| Auth | JWT (Flask-JWT-Extended) |
| PDF | ReportLab |
| Dataset | [Kaggle — Mobile Usage ScreenTime Dataset](https://www.kaggle.com/datasets/youssmanaveed/mobile-usage-screentime-dataset) |

---

## 📁 Project Structure

```
antigravity/
├── app.py                              # Main Flask application
├── config.py                           # Configuration settings
├── requirements.txt                    # Python dependencies
├── .env                                # Environment variables (OpenAI API key, MongoDB, etc.)
├── Mobile_Usage_Screentime_Dataset_.xlsx  # Kaggle source dataset
│
├── database/
│   ├── __init__.py
│   └── db.py                           # MongoDB connection, schema, seeding
│
├── models/
│   ├── __init__.py
│   ├── ml_model.py                     # Random Forest training & prediction
│   ├── convert_kaggle_dataset.py       # Kaggle dataset → project format converter
│   ├── generate_dataset.py             # Synthetic dataset generator (fallback)
│   ├── addiction_dataset.csv            # Training data (generated from Kaggle)
│   ├── addiction_model.pkl              # Trained model (auto-generated)
│   └── label_encoder.pkl               # Label encoder (auto-generated)
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py                  # Register, Login, Logout
│   ├── user_routes.py                  # Dashboard, Assessment, Progress, Tips
│   └── admin_routes.py                 # Admin Dashboard, Users, ML Panel
│
├── utils/
│   ├── __init__.py
│   ├── nlp_engine.py                   # OpenAI GPT Sentiment Analysis
│   └── pdf_generator.py                # PDF report generation
│
├── templates/
│   ├── base.html                       # Base template
│   ├── index.html                      # Landing page
│   ├── login.html / register.html      # Authentication pages
│   ├── dashboard.html                  # User dashboard
│   ├── assessment.html                 # Assessment form
│   ├── results.html                    # Results display
│   ├── progress.html                   # Progress history
│   ├── tips.html                       # Health tips
│   ├── feedback.html                   # Feedback form
│   ├── admin_dashboard.html            # Admin dashboard
│   ├── admin_users.html                # User management
│   ├── admin_content.html              # Content manager
│   ├── admin_ml_panel.html             # ML control panel
│   └── admin_feedback.html             # Feedback review
│
└── static/
    ├── css/style.css                   # Custom dark theme CSS
    └── js/scripts.js                   # Animations & interactions
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- MongoDB (local or Atlas)
- pip

### Installation

```bash
# 1. Navigate to project
cd antigravity

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your OpenAI API key in .env
# OPENAI_API_KEY=sk-your-key-here

# 5. Convert the Kaggle dataset (first time only)
python models/convert_kaggle_dataset.py

# 6. Start MongoDB
# Make sure MongoDB is running on localhost:27017

# 7. Run the application
python app.py
```

The app will:
- Initialize the database and seed default data
- Train the Random Forest model on the Kaggle-derived dataset (720 samples — 120 real + 5x augmented)
- Start the Flask server on `http://localhost:5000`

### Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@addictaware.com | admin123 |

---

## 🔮 System Workflow

```
User → Assessment Form
         ↓
    Data → MongoDB
         ↓
    Random Forest → Addiction Level (Low/Medium/High)
    OpenAI GPT → Sentiment Analysis (Positive/Negative/Neutral)
         ↓
    Results: Score + Emotion + Tips + Progress Chart
         ↓
    Admin Panel: Monitoring + Analytics + Retraining
```

---

## 📊 ML Model Details

### Dataset
- **Source**: [Kaggle — Mobile Usage ScreenTime Dataset](https://www.kaggle.com/datasets/youssmanaveed/mobile-usage-screentime-dataset) (CC0: Public Domain)
- **Size**: 120 real-world samples from 100+ users
- **Features Used**:

| Kaggle Column | Mapped Feature | Description |
|---|---|---|
| `Daily_ScreenTime_Hours` | `screen_time` | Daily screen time in hours |
| `Messages_Sent` | `phone_pickups` | Number of messages sent per day |
| `SocialMedia_Min` | `social_media_time` | Social media usage (converted from min to hours) |

- **Target**: `addiction_level` (Low / Medium / High) — derived from a weighted composite score

### Random Forest Classifier
- **Algorithm**: Random Forest with 100 estimators
- **Training Data**: 720 samples (120 real + 5x augmentation with noise)
- **Label Derivation**: KMeans clustering on standardized features
- **Accuracy**: ~93.75%
- **Feature Importance**: social_media_time (46.7%) > screen_time (42.4%) > phone_pickups (10.9%)

### OpenAI GPT Sentiment Analysis
- Uses GPT-3.5-turbo for context-aware sentiment classification
- Returns: Compound score (-1 to 1), Sentiment label, Emotion emoji
- Falls back to keyword-based analysis if the API is unavailable

---

## 🎨 Design System

- **Theme**: Dark mode with neon accents
- **Primary**: `#6C63FF` (Purple)
- **Accent**: `#00F5D4` (Teal/Neon)
- **Background**: `#0F172A` (Dark Navy)
- **Typography**: Inter + Poppins (Google Fonts)
- **Components**: Glassmorphism cards, animated score meters, gradient buttons
- **Animations**: Scroll reveal, floating elements, counter animations

---

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/login` | User login |
| GET/POST | `/register` | User registration |
| GET | `/logout` | Logout |
| GET | `/dashboard` | User dashboard |
| GET/POST | `/assessment` | Take assessment |
| GET | `/results` | View results |
| GET | `/progress` | Progress history |
| GET | `/download-report` | Download PDF report |
| GET/POST | `/feedback` | Submit feedback |
| GET | `/tips` | Health tips |
| GET | `/api/progress-data` | Chart data API |
| GET | `/admin/dashboard` | Admin dashboard |
| GET | `/admin/users` | User management |
| POST | `/admin/users/delete/<id>` | Delete user |
| GET/POST | `/admin/content` | Content manager |
| GET | `/admin/ml-panel` | ML control panel |
| POST | `/admin/retrain` | Retrain model |
| GET | `/admin/feedback` | Feedback review |
| GET | `/admin/api/analytics` | Analytics API |

---

## 🔒 Security

- Passwords hashed with bcrypt
- JWT-based session management
- Role-based access control (User / Admin)
- Form validation (client & server side)
- CORS enabled

---

## 📄 License

This project is for educational and portfolio purposes.

---

#   a d d i c t - a w a r e  
 