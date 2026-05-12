# CreditIQ-loan-eligibility-platform
AI-powered Loan Eligibility Prediction System using Python Flask &amp; Random Forest ML
# 🧠 CreditIQ — Smart Loan Eligibility Prediction System

> An AI-powered full-stack Loan Eligibility Prediction system built with Python Flask and Random Forest ML achieving **92% accuracy**.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![ML](https://img.shields.io/badge/ML-Random%20Forest-orange?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/Accuracy-92%25-brightgreen?style=for-the-badge)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 📌 About the Project

**CreditIQ** is a smart banking web application that predicts loan eligibility using Machine Learning. It analyzes applicant details like CIBIL score, income, employment type, and credit history to provide instant approval predictions with **92% accuracy**.

Built as **Project 3** for the **Hex Softwares Internship Program**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ⚡ **ML Prediction** | Random Forest model with 92% accuracy |
| 📊 **Live Dashboard** | Overview, Reports, History & Profile tabs |
| 📄 **PDF Report** | Download styled prediction report |
| 📧 **Email Notification** | Get results via Gmail SMTP |
| 💡 **Eligibility Tips** | Smart suggestions based on prediction result |
| 📈 **Progress Tracker** | Step-by-step application status |
| 💰 **EMI Calculator** | Interactive sliders with live charts |
| 🏦 **Affordability Check** | Live income vs EMI ratio bar |
| 🤖 **Chatbot Assistant** | Loan Q&A chatbot |
| 🔐 **Authentication** | Secure login & register system |
| ⚙️ **Admin Panel** | Manage users, view all predictions & analytics |
| 🎉 **Confetti** | Celebration animation on loan approval |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js |
| **Backend** | Python 3.14, Flask |
| **ML Model** | Scikit-learn (Random Forest Classifier) |
| **Database** | SQLite3 |
| **Email** | Gmail SMTP |
| **PDF** | ReportLab |
| **Auth** | Flask Session + SHA256 Password Hashing |

---

## 📁 Project Structure

```
CreditIQ/
├── app.py               ← Flask REST API & routes
├── model.py             ← Random Forest ML model
├── database.py          ← SQLite database operations
├── auth.py              ← Login, register, logout routes
├── pdf_report.py        ← PDF report generator
├── mailer.py            ← Gmail email notifications
├── requirements.txt     ← Python dependencies
├── dataset/
│   └── loan_data.csv    ← Kaggle loan dataset
├── model/
│   └── loan_model.pkl   ← Trained ML model (auto-generated)
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── index.html       ← Main dashboard
    ├── login.html       ← Login page
    ├── register.html    ← Register page
    └── admin.html       ← Admin panel
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Shahinshafi1717/CreditIQ-loan-eligibility-platform.git
cd CreditIQ-loan-eligibility-platform
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add dataset (optional but recommended)
- Download from: [Kaggle Loan Prediction Dataset](https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset)
- Place `train.csv` in `dataset/` folder and rename to `loan_data.csv`
- If no dataset provided, model auto-trains on synthetic data

### 5. Configure email notifications (optional)
Open `mailer.py` and update:
```python
GMAIL_USER = "your_gmail@gmail.com"
GMAIL_PASS = "your_app_password"  # Gmail App Password
```

### 6. Run the application
```bash
python app.py
```
Open: **http://127.0.0.1:5000**

---

## 🔐 Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| 👑 Admin | `admin` | `admin123` |
| 👤 User | Register yourself | — |

---

## 📊 ML Model Details

| Item | Details |
|------|---------|
| **Algorithm** | Random Forest Classifier |
| **Accuracy** | **92%** |
| **Estimators** | 200 trees |
| **Dataset** | Kaggle Loan Prediction Dataset |
| **Top Feature** | CIBIL Score (30.6% importance) |
| **2nd Feature** | Credit History (27.3% importance) |
| **Total Features** | 12 features |

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/predict` | Run loan eligibility prediction |
| `GET` | `/api/history` | Get prediction history |
| `GET` | `/api/stats` | Get summary statistics |
| `POST` | `/api/download-pdf` | Download PDF report |
| `GET` | `/api/admin/users` | Get all users (admin only) |
| `DELETE` | `/api/admin/users/<id>` | Delete user (admin only) |
| `GET` | `/api/admin/stats` | Admin statistics |

---

## 📸 App Preview

### 🔐 Login Page
- Professional green banking theme
- Secure authentication system

### 📊 Dashboard
- **Overview** — Animated stats, donut chart, recent activity
- **Predict** — Loan form with live affordability check
- **History** — Searchable prediction history table
- **Reports** — Analytics charts & CIBIL distribution
- **EMI Calculator** — Interactive loan calculator
- **Profile** — User stats & account management

### ⚙️ Admin Panel
- User management with delete functionality
- All predictions across all users
- Analytics & approval rate charts

---

## 🚀 Future Improvements

- [ ] Deploy online (Render / Railway)
- [ ] Add XGBoost model for comparison
- [ ] Export predictions to Excel/CSV
- [ ] Add forgot password feature
- [ ] Mobile responsive design improvements

---

## 👨‍💻 Author

**Shahin Shafi**
- GitHub: [@Shahinshafi1717](https://github.com/Shahinshafi1717)
- Project built for: **Hex Softwares Internship — Project 3**

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and modify for educational purposes.

---

## 🙏 Acknowledgements

- [Kaggle](https://www.kaggle.com) — Loan Prediction Dataset
- [Scikit-learn](https://scikit-learn.org) — ML Library
- [Flask](https://flask.palletsprojects.com) — Web Framework
- [Chart.js](https://www.chartjs.org) — Charts & Visualizations
- [ReportLab](https://www.reportlab.com) — PDF Generation

---

⭐ **If you found this project helpful, please give it a star on GitHub!**
