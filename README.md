# 💳 Credit Card Fraud Detection System

A web-based application that uses Machine Learning to detect fraudulent credit card transactions in real time. The system allows users to register, log in, analyze individual transactions, and upload CSV files for batch fraud detection.

---

## ✨ Features

- 🔐 User registration and login with secure password hashing
- 🤖 Real-time fraud prediction using a trained Random Forest model
- 📂 Batch detection through CSV file upload
- 📊 Transaction confidence score and status messages
- 📩 Contact form with database storage
- 🖥️ Session-based dashboard
- 🗄️ MySQL database integration

---

## 🛠️ Technology Stack

- 🐍 Python 3
- 🌐 Flask
- 🗄️ MySQL
- 🤖 Scikit-learn
- 📊 Pandas
- 🔢 NumPy
- 🎨 HTML / CSS / Bootstrap

---

## 🧠 Machine Learning Model

The application uses a pre-trained Random Forest classifier along with a scaler to process the following features:

- `V1` to `V28`
- `Amount`

The model predicts whether a transaction is:

- 🚨 **Fraudulent Transaction**
- ✅ **Genuine Transaction**

## 📦 Required Python Packages

Flask 2.3.3
mysql-connector-python 8.3.0
Werkzeug 2.3.7
pandas 2.2.2
numpy 1.26.4
scikit-learn 1.4.2

## 🗄️ Database Setup

This project uses MySQL to store user accounts and contact messages.

Create a new MySQL database named fraud_detection.
Update your database credentials in the .env file.
Import the provided SQL schema file:
mysql -u root -p fraud_detection < schema.sql

### 👨‍💻 Author
              - Abhishek Nagle

### 📜 License 
      This project is developed for academic and educational purposes.


## ⚙️ Installation

### 📥 Clone the Repository

```bash
git clone https://github.com/your-username/credit-card-fraud-detection.git
cd credit-card-fraud-detection
```

🐍 Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

🗄️ Set Up the Database

mysql -u root -p fraud_detection < schema.sql

▶️ Running the Application
python main.py

🌍 The Application Will Be Available At http://127.0.0.1:5000/
```
---

## 📁 Project Structure

```text
.
├── main.py
├── requirements.txt
├── .env
├── schema.sql
├── model/
│   ├── random_forest_model.pkl
│   └── scaler.pkl
├── templates/
├── static/
├── Uploads/
└── Major_Project_Sem_4_Report.pdf
