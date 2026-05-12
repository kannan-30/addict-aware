# Addict Aware 🛡️

> **AI-powered digital wellness platform** that predicts addiction levels and analyzes emotional patterns using Machine Learning and Natural Language Processing.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

---

## 🚀 Key Features

### 🤖 AI & Machine Learning Core
- **Predictive Engine (~93.8% Accuracy)** — Features a custom-trained **Random Forest Classifier** that evaluates real-world screen time data (hours spent, phone pickups, social media usage) to predict digital addiction levels (Low, Medium, High).
- **Sentiment Analysis** — Utilizes **OpenAI's GPT-3.5-turbo** to analyze qualitative emotional feedback, uncovering hidden sentiment patterns and correlating them with digital behaviors.

### 👤 User Module
- **Smart Assessment** — Log digital habits and emotional states through an intuitive interface.
- **Progress Tracking** — Visualize your journey with interactive **Chart.js** dashboards.
- **PDF Reports** — Download dynamic health reports generated with **ReportLab**.
- **Personalized Tips** — Receive behavioral recommendations tailored to your prediction level.

### 🛠️ Admin Module
- **Analytics Dashboard** — Monitor platform KPIs, user distributions, and system health.
- **User Management** — Full CRUD capabilities for managing user accounts.
- **Content Manager** — Dynamic management of awareness health tips.
- **ML Control Panel** — Monitor model performance and trigger retraining on the fly.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9+, Flask 3.0 |
| **Database** | MongoDB (PyMongo) |
| **ML Model** | Random Forest Classifier (scikit-learn) |
| **NLP** | OpenAI GPT-3.5-turbo |
| **Frontend** | HTML5, CSS3, Bootstrap 5 (Custom Dark Theme) |
| **Visuals** | Chart.js, Lucide Icons |
| **Auth** | JWT (Flask-JWT-Extended) |
| **Reports** | ReportLab |

---

## 📁 Project Structure

```text
addict_aware/
├── app.py                  # Flask Application Entry Point
├── config.py               # Configuration Settings
├── requirements.txt        # Dependencies
├── .env                    # Environment Variables
├── database/               # Database logic & seeding
├── models/                 # ML Models & Data conversion
├── routes/                 # Flask Blueprints (Auth, User, Admin)
├── utils/                  # NLP Engine & PDF Generation
├── templates/              # HTML Templates (Jinja2)
└── static/                 # CSS & JS Assets
```

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/kannan-30/addict-aware.git
cd addict-aware
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory and add your credentials:
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-key
OPENAI_API_KEY=sk-your-openai-key
MONGO_URI=mongodb://localhost:27017/addict_aware
```

### 5. Run the App
```bash
python app.py
```
*The system will automatically initialize the database and train the ML model on first run.*

---

## 📊 Default Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@addictaware.com` | `admin123` |

---

## 📄 License
This project is for educational and portfolio purposes.

Developed with ❤️ by [kannan-30](https://github.com/kannan-30)