from flask import Flask, render_template
import mysql.connector
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="event_ticketing"
    )
    return conn
app=Flask(__name__)
@app.route('/')
def home():
    return render_template("home.html")
@app.route('/test_db')
def test_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 'Database Connected Successfully!'")
    result = cur.fetchone()
    conn.close()
    return result[0]
@app.route('/events')
def show_events():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT event_id, event_name, category_id, date, venue FROM events")
    data = cur.fetchall()
    conn.close()
    return render_template("events.html", events=data)
@app.route('/event/<int:event_id>')
def event_details(event_id):
    conn = get_connection()
    cur = conn.cursor()
    # 1️Fetch selected event
    cur.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    event = cur.fetchone()
    if not event:
        conn.close()
        return "<h2>Event Not Found</h2>", 404
    # 2️⃣ FETCH STUDENTS (⬅⬅ THIS IS THE PART YOU ASKED ABOUT)
    cur.execute("SELECT student_id, name FROM students")
    students = cur.fetchall()
    conn.close()
    # 3️⃣ Send BOTH event and students to template
    return render_template(
        "event_details.html",
        event=event,
        students=students
    )
import qrcode
import os
from flask import request
@app.route('/register/<int:event_id>', methods=['POST'])
def register(event_id):
    # 1️⃣ get selected student
    student_id = request.form['student_id']
    # 2️⃣ CONNECT TO DATABASE (THIS WAS MISSING)
    conn = get_connection()
    cur = conn.cursor()
    # 3️⃣ insert registration
    cur.execute(
        "INSERT INTO registrations (student_id, event_id, qr_code) VALUES (%s, %s, '')",
        (student_id, event_id)
    )
    conn.commit()
    # 4️⃣ get auto-generated reg_id
    reg_id = cur.lastrowid
    # 5️⃣ generate QR
    qr_text = str(reg_id)
    img = qrcode.make(qr_text)
    qr_filename = f"qr_{reg_id}.png"
    qr_path = os.path.join("static", qr_filename)
    img.save(qr_path)
    # 6️⃣ update qr filename in DB
    cur.execute(
        "UPDATE registrations SET qr_code=%s WHERE reg_id=%s",
        (qr_filename, reg_id)
    )
    conn.commit()

    # 7️⃣ close connection
    conn.close()

    # 8️⃣ render ticket
    return render_template(
        "ticket.html",
        event_id=event_id,
        reg_id=reg_id,
        qr_filename=qr_filename
    )
@app.route('/scan')
def scan():
    return render_template("scanner.html")

from flask import request

@app.route('/validate_qr', methods=['POST'])
def validate_qr():
    data = request.get_json()
    qr_value = data.get("qr_data")  # reg_id

    conn = get_connection()
    cur = conn.cursor()

    # check registration exists & get student_id
    cur.execute("""
        SELECT student_id 
        FROM registrations 
        WHERE reg_id = %s
    """, (qr_value,))
    
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Invalid Ticket"
    student_id = row[0]
    # get student name
    cur.execute("SELECT name FROM students WHERE student_id = %s", (student_id,))
    student = cur.fetchone()[0]
    # insert check-in
    cur.execute("INSERT INTO checkins (reg_id) VALUES (%s)", (qr_value,))
    conn.commit()
    conn.close()
    return f"Check-in Successful! Student: {student}"
@app.route('/admin')
def admin_dashboard():
    conn = get_connection()
    cur = conn.cursor()
    # 1. Fetch all registrations with student + event details
    cur.execute("""
        SELECT r.reg_id, s.name, e.event_name, e.date
        FROM registrations r
        JOIN students s ON r.student_id = s.student_id
        JOIN events e ON r.event_id = e.event_id
        ORDER BY r.reg_id DESC
    """)
    registrations = cur.fetchall()
    # 2. Fetch all check-ins with student + event
    cur.execute("""
        SELECT s.name, e.event_name, c.checkin_time
        FROM checkins c
        JOIN registrations r ON c.reg_id = r.reg_id
        JOIN students s ON r.student_id = s.student_id
        JOIN events e ON r.event_id = e.event_id
        ORDER BY c.checkin_time DESC
    """)
    checkins = cur.fetchall()
    conn.close()
    return render_template("admin.html", registrations=registrations, checkins=checkins)
from flask import redirect, url_for
@app.route('/reset_registrations')
def reset_registrations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM registrations")
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))
if __name__== '__main__':
    app.run(debug=True)