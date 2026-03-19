from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model doktora
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)

# Model termina
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    hour = 
db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10), nullable=False)

# Kreiranje baze ako ne postoji
with app.app_context():
    db.create_all()
    # Dodavanje doktora ako nema
    if Doctor.query.count() == 0:
        db.session.add_all([
            Doctor(name="Dr. Marković", color="lightblue"),
            Doctor(name="Dr. Petrović", color="lightgreen"),
            Doctor(name="Dr. Jovanović", color="lightcoral")
        ])
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    today = str(date.today())
    if request.method == 'POST':
        hour = int(request.form['hour'])
        doctor_id = int(request.form['doctor'])
        title = request.form['title']
        new_appt = Appointment(doctor_id=doctor_id, title=title, hour=hour, date=today)
        db.session.add(new_appt)
        db.session.commit()
        return redirect('/')

    doctors = Doctor.query.all()
    appointments = {appt.hour: appt for appt in Appointment.query.filter_by(date=today).all()}
    return render_template('index.html', doctors=doctors, appointments=appointments)

if __name__ == "__main__":
    # Za deploy na Render / Railway koristi 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=True)
