import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vihar:vihar@db:5432/ems'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Retry database connection
connected = False
for _ in range(5):
    try:
        db.create_all()
        connected = True
        break
    except Exception as e:
        print(f"Database connection failed: {e}. Retrying...")
        time.sleep(5)

if not connected:
    raise Exception("Could not connect to the database after multiple attempts.")

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    position = db.Column(db.String(80), nullable=False)

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    new_employee = Employee(name=data['name'], email=data['email'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee added successfully!'})

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = [{'id': e.id, 'name': e.name, 'email': e.email, 'position': e.position} for e in employees]
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
