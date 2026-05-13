# Credit Card Fraud Detection System

A web-based application that uses Machine Learning to detect fraudulent credit card transactions in real time. The system allows users to register, log in, analyze individual transactions, and upload CSV files for batch fraud detection.

## Features

- User registration and login with secure password hashing
- Real-time fraud prediction using a trained Random Forest model
- Batch detection through CSV file upload
- Transaction confidence score and status messages
- Contact form with database storage
- Session-based dashboard
- MySQL database integration

## Technology Stack

- Python 3
- Flask
- MySQL
- Scikit-learn
- Pandas
- NumPy
- HTML/CSS/Bootstrap

## Machine Learning Model

The application uses a pre-trained Random Forest classifier along with a scaler to process the following features:

- `V1` to `V28`
- `Amount`

The model predicts whether a transaction is:

- **Fraudulent Transaction**
- **Genuine Transaction**

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── .env
├── model/
│   ├── random_forest_model.pkl
│   └── scaler.pkl
├── templates/
├── static/
├── Uploads/
└── Major_Project_Sem_4_Report.pdf
----

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/credit-card-fraud-detection.git
cd credit-card-fraud-detection

---
## Create and Activate a Virtual Environment

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Running the Application
python main.py

## The application will be available at:
http://127.0.0.1:5000/
---

## Required Python Packages
Flask 2.3.3
mysql-connector-python 8.3.0
Werkzeug 2.3.7
pandas 2.2.2
numpy 1.26.4
scikit-learn 1.4.2
---

## Database Setup

This project uses MySQL to store user accounts and contact messages.

1. Create a new MySQL database named `fraud_detection`.
2. Update your database credentials in the `.env` file.
3. Import the provided SQL schema file:

```bash
mysql -u root -p fraud_detection < schema.sql
---


## Author

## Abhishek Nagle

## License
This project is developed for academic and educational purposes.

## Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Login Page
![Login Page](screenshots/login.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Prediction Result
![Prediction Result](screenshots/prediction.png)

### CSV Upload
![CSV Upload](screenshots/upload.png)

### Batch Results
![Batch Results](screenshots/results.png)

