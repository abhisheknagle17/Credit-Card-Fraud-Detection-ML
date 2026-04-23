from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
import os
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# MySQL connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)

# Register Page
@app.route('/register.html', methods=['GET', 'POST'])
def register_html():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        try:
            cursor.execute(
                "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, password)
            )
            db.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('login_html'))
        except mysql.connector.IntegrityError:
            flash("Email already registered!", "danger")
    return render_template('register.html')

# Login Page
@app.route('/login.html', methods=['GET', 'POST'])
def login_html():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            if check_password_hash(user['password'], password_input):
                session['user_id'] = user['id']
                flash("Login successful!", "success")
                return redirect(url_for('dashboard_html'))
            else:
                flash("Invalid Password", "danger")
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login_html'))

# Dashboard (Protected)
@app.route('/dashboard.html')
def dashboard_html():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login_html'))
    cursor.execute("SELECT first_name, last_name FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    return render_template('dashboard.html', user=user)

# Contact Form
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        try:
            cursor.execute(
                "INSERT INTO contact_messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                (name, email, subject, message)
            )
            db.commit()
            flash("Message sent successfully!", "success")
        except Exception as e:
            print(f"Error in contact form: {e}")
            flash("An error occurred while sending the message.", "danger")
        return redirect(url_for('contact'))
    return render_template('contact.html')

# Public Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/detection_result.html')
def result():
    return render_template(
        'detection_result.html',
        transactions=None,
        amount='N/A',
        timestamp='N/A',
        location='Unknown',
        card_holder='Anonymous',
        prediction_result='N/A'
    )

@app.route('/service.html')
def service():
    return render_template('service.html')

@app.route('/project.html')
def project_html():
    return render_template('project.html')

@app.route('/feature.html')
def feature():
    return render_template('feature.html')

@app.route('/team.html')
def team():
    return render_template('team.html')

@app.route('/testimonial.html')
def testimonial():
    return render_template('testimonial.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/upload.html')
def upload():
    return render_template('upload.html')

@app.route('/forgot-password.html')
def forgot_pass():
    return render_template('forgot-password.html')

@app.route('/check-transaction.html')
def check():
    return render_template('check-transaction.html')

@app.route('/test-404')
def trigger_404():
    abort(404)

@app.route('/dataset')
def dataset():
    return "This is the dataset page."

@app.route('/user')
def user():
    return "This is the User Module page."

@app.route('/fraud')
def fraud():
    return "This is the Fraud Detection Module page."

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/predict.html', methods=['GET', 'POST'])
def predict_transaction():
    if request.method == 'POST':
        try:
            input_data = [float(request.form[col]) for col in feature_columns]
            input_df = pd.DataFrame([input_data], columns=feature_columns)
            scaled_input = scaler.transform(input_df)
            prediction = rf_model.predict(scaled_input)[0]
            model_name = 'Random Forest'
            result = "Fraudulent Transaction" if prediction == 1 else "Genuine Transaction"
            return render_template('detection_result.html', prediction_result=result, model=model_name)
        except Exception as e:
            flash(f"Error in prediction: {str(e)}", "danger")
            return redirect(url_for('predict_transaction'))
    return render_template('predict.html', feature_columns=feature_columns)

# Machine Learning Model Loading
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
with open(os.path.join(MODEL_DIR, 'random_forest_model.pkl'), 'rb') as f:
    rf_model = pickle.load(f)
with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'rb') as f:
    scaler = pickle.load(f)
feature_columns = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
                   'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
                   'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']

# Allowed file extensions for upload
def allowed_file(filename):
    return filename.lower().endswith('.csv')

# Update the /upload-detect route
@app.route('/upload-detect', methods=['POST'])
def upload_and_detect():
    if 'transaction_file' not in request.files:
        flash("No file part in the request.", "danger")
        return redirect(url_for('upload'))

    file = request.files['transaction_file']
    if file.filename == '':
        flash("No selected file.", "danger")
        return redirect(url_for('upload'))

    if not allowed_file(file.filename):
        flash("Please upload a valid CSV file.", "danger")
        return redirect(url_for('upload'))

    try:
        uploads_dir = os.path.join(app.root_path, 'Uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        filepath = os.path.join(uploads_dir, file.filename)
        file.save(filepath)
        print(f"[INFO] File saved: {filepath}")

        # Read and validate CSV
        try:
            df = pd.read_csv(filepath, dtype_backend='numpy_nullable')
            df.columns = df.columns.str.strip()
            print(f"[INFO] CSV columns: {df.columns.tolist()}")
            print(f"[INFO] Number of rows: {len(df)}")
        except Exception as e:
            flash(f"Failed to read CSV file: {str(e)}", "danger")
            print(f"[ERROR] CSV reading failed: {str(e)}")
            return redirect(url_for('upload'))

        if df.empty:
            flash("The CSV file is empty.", "danger")
            print("[ERROR] Empty CSV file detected.")
            return redirect(url_for('upload'))

        # Validate required columns
        missing_cols = [col for col in feature_columns if col not in df.columns]
        if missing_cols:
            flash(f"Missing required columns in CSV: {', '.join(missing_cols)}", "danger")
            print(f"[ERROR] Missing columns: {missing_cols}")
            return redirect(url_for('upload'))

        transactions_info = []
        error_messages = []

        for index, row in df.iterrows():
            try:
                input_data = []
                for col in feature_columns:
                    value = row[col]
                    if pd.isna(value) or value == '':
                        raise ValueError(f"Missing or empty value in column '{col}' at row {index+1}")
                    try:
                        float_value = float(value)
                        input_data.append(float_value)
                    except (ValueError, TypeError) as e:
                        raise ValueError(f"Non-numeric value in column '{col}' at row {index+1}: {value}")

                input_array = np.array(input_data).reshape(1, -1)
                print(f"[DEBUG] Input array for row {index+1}: {input_array}")

                try:
                    scaled = scaler.transform(input_array)
                    print(f"[DEBUG] Scaled input for row {index+1}: {scaled}")
                    pred = rf_model.predict(scaled)[0]
                    confidence = rf_model.predict_proba(scaled)[0][pred] * 100
                except Exception as e:
                    raise ValueError(f"Model processing failed at row {index+1}: {str(e)}")

                result = "Fraud" if pred == 1 else "Secure and Safe"
                message = (
                    "This transaction is flagged as fraudulent. Please review immediately."
                    if pred == 1 else
                    "This transaction appears safe and secure."
                )

                transactions_info.append({
                    'transaction_id': str(row.get('transaction_id', f'TXN{index+1:04d}')),
                    'amount': f"₹{float(row.get('Amount', 0)):.2f}",
                    'timestamp': str(row.get('time', 'N/A')),
                    'location': str(row.get('location', 'Unknown')),
                    'card_holder': str(row.get('card_holder', 'Anonymous')),
                    'prediction_result': result,
                    'prediction_probability': f"{confidence:.2f}%",
                    'status_message': message
                })
                print(f"[OK] Transaction {index+1} processed successfully.")

            except Exception as e:
                error_messages.append(f"Row {index+1}: {str(e)}")
                print(f"[ERROR] Skipping transaction {index+1}: {str(e)}")
                continue

        if not transactions_info:
            error_summary = "; ".join(error_messages) if error_messages else "Unknown error in processing rows."
            flash(f"No valid transactions processed. {len(error_messages)} row(s) failed. Errors: {error_summary}", "warning")
            print(f"[ERROR] All {len(df)} rows failed. Error details: {error_summary}")
            return redirect(url_for('upload'))

        flash(f"Processed {len(transactions_info)} transaction(s) successfully.", "success")
        first = transactions_info[0]
        return render_template(
            'detection_result.html',
            transactions=transactions_info,
            amount=first['amount'],
            timestamp=first['timestamp'],
            location=first['location'],
            card_holder=first['card_holder'],
            prediction_result=first['prediction_result']
        )

    except Exception as e:
        print(f"[FATAL] Error processing file: {str(e)}")
        flash(f"Internal error processing CSV: {str(e)}", "danger")
        return redirect(url_for('upload'))

# Run App
if __name__ == '__main__':
    app.run(debug=False)
