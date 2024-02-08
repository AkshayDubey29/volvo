from flask import Flask, request, render_template_string, redirect, url_for, jsonify
from flask_httpauth import HTTPBasicAuth
import pymysql
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# Database name
DATABASE_NAME = 'ebdb'

# Retrieve database connection info from environment variables
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = int(os.getenv('MYSQL_PORT', 3306))  # Default MySQL port is 3306
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')

@auth.verify_password
def verify_password(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return username

def get_db_connection():
    return pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, 
                           db=DATABASE_NAME, port=mysql_port, charset='utf8mb4', 
                           cursorclass=pymysql.cursors.DictCursor)

def create_database_and_table():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(DATABASE_NAME))
            cursor.execute("USE {}".format(DATABASE_NAME))
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    experience VARCHAR(50),
                    feedback TEXT NOT NULL,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()
    finally:
        conn.close()

# Call this function directly to initialize the database
create_database_and_table()

@app.route('/admin')
@auth.login_required
def admin():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM feedback")
            feedback_data = cursor.fetchall()
        return jsonify(feedback_data)
    finally:
        conn.close()

@app.route('/')
def feedback_form():
    # Feedback form HTML content with styles goes here
    feedback_form_html = """

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Feedback Form</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                background: #fff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
            h2, h4 {
                text-align: center;
                color: #333;
            }
            form {
                display: flex;
                flex-direction: column;
            }
            label {
                margin-top: 10px;
                margin-bottom: 5px;
                color: #333;
            }
            input[type=text], textarea {
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            .radio-group {
                display: flex;
                justify-content: space-between;
                margin-top: 5px;
            }
            .radio-group label {
                flex: 1;
                margin-right: 20px;
                background: #f7f7f7;
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
                border-radius: 5px;
                cursor: pointer;
            }
            .radio-group input[type="radio"] {
                display: none;
            }
            .radio-group input[type="radio"]:checked + label {
                background: #e9e9e9;
                border-color: #ccc;
            }
            input[type=submit] {
                padding: 10px 15px;
                background-color: #5cb85c;
                border: none;
                border-radius: 5px;
                color: white;
                cursor: pointer;
                margin-top: 15px;
                font-size: 16px;
            }
            input[type=submit]:hover {
                background-color: #4cae4c;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Feedback Form</h2>
            <h4>For Akshay Dubey, Engineering Manager Position</h4>
            <form action="/submit" method="post">
                <label for="name">Your Name:</label>
                <input type="text" id="name" name="name" required>
                
                <label>Experience Rating:</label>
                <div class="radio-group">
                    <input type="radio" id="excellent" name="experience" value="excellent" required>
                    <label for="excellent">Excellent</label>
                    
                    <input type="radio" id="good" name="experience" value="good">
                    <label for="good">Good</label>
                    
                    <input type="radio" id="fair" name="experience" value="fair">
                    <label for="fair">Fair</label>
                    
                    <input type="radio" id="poor" name="experience" value="poor">
                    <label for="poor">Poor</label>
                </div>
                
                <label for="feedback">Your Feedback:</label>
                <textarea id="feedback" name="feedback" rows="4" cols="50" required></textarea>
                
                <input type="submit" value="Submit Feedback">
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(feedback_form_html)

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    experience = request.form.get('experience')
    feedback = request.form['feedback']
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO feedback (name, experience, feedback) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, experience, feedback))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for('feedback_form'))

# Replace the placeholder with the actual HTML content for FEEDBACK_FORM

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
