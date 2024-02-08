from flask import Flask, request, render_template_string, redirect, url_for
import pymysql
import os

app = Flask(__name__)

# Retrieve database connection info from environment variables
mysql_host = os.getenv('MYSQL_HOST')
mysql_db = os.getenv('MYSQL_DB')
mysql_port = int(os.getenv('MYSQL_PORT', 3306))  # Default MySQL port is 3306
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')

def insert_feedback(name, feedback):
    conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, 
                           db=mysql_db, port=mysql_port, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO feedback (name, feedback) VALUES (%s, %s)"
            cursor.execute(sql, (name, feedback))
        conn.commit()
    finally:
        conn.close()

FEEDBACK_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Feedback Form</title>
</head>
<body>
    <h2>Feedback on Platform Engineer Practical Test</h2>
    <form action="/submit" method="post">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name" required><br>
        <label for="feedback">Feedback:</label><br>
        <textarea id="feedback" name="feedback" rows="4" cols="50" required></textarea><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/')
def feedback_form():
    return render_template_string(FEEDBACK_FORM)

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    feedback = request.form['feedback']
    # Insert the feedback into the database
    insert_feedback(name, feedback)
    return redirect(url_for('feedback_form'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80, debug=True)
