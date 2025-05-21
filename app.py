from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from scrape import scrape_events
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

db_url = os.getenv('DATABASE_URL')
if not db_url:
    raise ValueError("DATABASE_URL environment variable not set")

app = Flask(__name__)

# PostgreSQL config via Railway
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for registration
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    event_id = db.Column(db.Integer)

# Main route
@app.route('/')
def index():
    events = scrape_events()
    return render_template('index.html', events=events)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    events = scrape_events()
    event = events[event_id]
    return render_template('event_details.html', event=event)

@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def registration_form(event_id):
    events = scrape_events()
    event = events[event_id]

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        new_reg = Registration(name=name, email=email, phone=phone, event_id=event_id)
        db.session.add(new_reg)
        db.session.commit()

        return redirect(event['Book Ticket'])

    return render_template('registration_form.html', event=event)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))