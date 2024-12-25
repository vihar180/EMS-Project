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
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO employees (name, position, date_joined) VALUES (%s, %s, %s)",
                   (data['name'], data['position'], data['date_joined']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Employee registered successfully!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
