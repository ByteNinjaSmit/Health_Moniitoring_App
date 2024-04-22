from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import tkinter as tk
import tkinter.simpledialog as simpledialog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blood_pressure = db.Column(db.String(10), nullable=False)
    heart_rate = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.String(10), nullable=False)

def create_user():
    username = simpledialog.askstring(title="Create User", prompt="Enter your username:")
    password = simpledialog.askstring(title="Create User", prompt="Enter your password:")
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'})

@app.route('/health-data', methods=['POST'])
def health_data():
    user_id = request.form['user_id']
    blood_pressure = request.form['blood_pressure']
    heart_rate = request.form['heart_rate']
    weight = request.form['weight']
    new_data = HealthData(user_id=user_id, blood_pressure=blood_pressure, heart_rate=heart_rate, weight=weight)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Health data saved'})

if __name__ == '__main__':
    db.create_all()
    create_user()
    app.run(debug=True)