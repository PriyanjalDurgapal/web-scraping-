from flask_mysql import MySQL

def init_db(mysql):
    """Initialize the MySQL connection and return it"""
    return mysql

def insert_registration(mysql, name, email, phone, event_id):
    """Insert the registration data into the database"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO registrations (name, email, phone, event_id) VALUES (%s, %s, %s, %s)",
                    (name, email, phone, event_id))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Database Error: {e}")
        return False
