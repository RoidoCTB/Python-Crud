from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database connection
def db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_student")
    students = cursor.fetchall()

    # Convert 'bdate' to datetime and calculate age
    students_list = []
    for student in students:
        student_dict = dict(student)  # Convert sqlite3.Row to dictionary
        bdate = datetime.strptime(student_dict['bdate'], '%Y-%m-%d')  # Convert 'bdate' to datetime object
        student_dict['age'] = datetime.now().year - bdate.year  # Calculate the age
        students_list.append(student_dict)  # Add updated dictionary to the list

    now = datetime.now()  # Include current date and time
    return render_template('index.html', students=students_list, now=now)




@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        fname = request.form['fname']
        bdate = request.form['bdate']
        gender = request.form['gender']
        email = request.form['email']

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbl_student (fname, bdate, gender, email) VALUES (?, ?, ?, ?)",
                       (fname, bdate, gender, email))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        fname = request.form['fname']
        bdate = request.form['bdate']
        gender = request.form['gender']
        email = request.form['email']

        cursor.execute("""UPDATE tbl_student
                          SET fname = ?, bdate = ?, gender = ?, email = ?
                          WHERE id = ?""", (fname, bdate, gender, email, id))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM tbl_student WHERE id = ?", (id,))
    student = cursor.fetchone()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_student WHERE id = ?", (id,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/view/<int:id>')
def view(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_student WHERE id = ?", (id,))
    student = cursor.fetchone()

    now = datetime.now()  # Include current date and time for view.html
    return render_template('view.html', student=student, now=now)

if __name__ == '__main__':
    app.run(debug=True)

