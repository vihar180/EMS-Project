from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    return mysql.connector.connect(
        host="database",
        user="root",
        password="root",
        database="employees"
    )

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        employee_id = f"EMP-{count + 1:04d}"

        cursor.execute(
            "INSERT INTO employees (id, name, position, date_joined, password) VALUES (%s, %s, %s, %s, %s)",
            (employee_id, data['name'], data['position'], data['date_joined'], data['password'])
        )
        connection.commit()

        return jsonify({"employee_id": employee_id, "message": "Registration successful!"}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM employees WHERE id = %s AND password = %s", (data['employee_id'], data['password']))
        user = cursor.fetchone()

        if user:
            return jsonify({"redirect": "home.html"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
