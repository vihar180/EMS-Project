from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="<DB_Private_IP>",
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
        count = cursor.fetchone()[0] + 1
        employee_id = f"EMP-{count:04}"

        query = "INSERT INTO employees (employee_id, name, position, date_joined, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (employee_id, data['name'], data['position'], data['date_joined'], data['password']))
        connection.commit()

        return jsonify({"employee_id": employee_id, "message": "Registration successful!"}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM employees WHERE employee_id = %s AND password = %s"
        cursor.execute(query, (data['employee_id'], data['password']))
        user = cursor.fetchone()

        if user:
            return jsonify({"message": "Login successful!", "redirect": "home.html"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
