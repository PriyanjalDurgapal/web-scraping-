from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from sceap import scrape_events  

app = Flask(__name__)

# MySQL Confi
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'root'  
app.config['MYSQL_DB'] = 'events' 

mysql = MySQL(app)

# Main routing
@app.route('/')
def index():
    events = scrape_events() 
    return render_template('index.html', events=events)

# Event details route
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
        
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO registrations (name, email, phone, event_id) VALUES (%s, %s, %s, %s)",
                    (name, email, phone, event_id))
        mysql.connection.commit()
        cur.close()
        
        
        ticket_url = event['Book Ticket']
        return redirect(ticket_url)

    return render_template('registration_form.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)
