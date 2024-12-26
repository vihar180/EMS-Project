from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="database",
        user="root",
        password="root",
        database="employees"
    )

@app.route('/')
def home():
    return "Welcome to the Employee Management System API!"

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        connection = get_db_connection()
        cursor = connection.cursor()

        # Validate required fields
        if not all([data.get('name'), data.get('position'), data.get('date_joined'), data.get('password')]):
            return jsonify({"message": "All fields are required"}), 400

        # Generate Employee ID
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        employee_id = f"EMP-{count + 1:04d}"

        # Insert into database
        cursor.execute(
            "INSERT INTO employees (id, name, position, date_joined, password) VALUES (%s, %s, %s, %s, %s)",
            (employee_id, data['name'], data['position'], data['date_joined'], data['password'])
        )
        connection.commit()

        cursor.close()
        connection.close()
        return jsonify({"message": f"Employee registered successfully! Employee ID: {employee_id}"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM employees WHERE id = %s AND password = %s", (data['employee_id'], data['password']))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return jsonify({"message": f"Welcome, {result[0]}!"}), 200
        else:
            return jsonify({"message": "Invalid Employee ID or Password."}), 401
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
