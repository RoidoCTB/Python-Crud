from flask import Flask, render_template, request, redirect, url_for, jsonify
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

    students_list = []
    for student in students:
        student_dict = dict(student)

        try:
            bdate = datetime.strptime(student_dict['bdate'], '%Y-%m-%d')
        except ValueError:
            bdate = datetime.strptime(student_dict['bdate'], '%d-%m-%Y')

        today = datetime.today()
        age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
        student_dict['age'] = age
        students_list.append(student_dict)

    return render_template('index.html', students=students_list)



# JSON API endpoint for GUI use
@app.route('/api/students', methods=['GET', 'POST'])
def api_students():
    if request.method == 'GET':
        # Handle GET request: Fetch students from the database
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_student")
        students = cursor.fetchall()

        students_list = []
        for student in students:
            student_dict = dict(student)

            try:
                bdate = datetime.strptime(student_dict['bdate'], '%Y-%m-%d')
            except ValueError:
                bdate = datetime.strptime(student_dict['bdate'], '%d-%m-%Y')

            today = datetime.today()
            age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
            student_dict['age'] = age
            students_list.append(student_dict)

        return jsonify(students_list)

    elif request.method == 'POST':
        # Handle POST request: Add a new student to the database
        data = request.get_json()
        fname = data.get('fname')
        bdate = data.get('bdate')
        gender = data.get('gender')
        email = data.get('email')

        # Check for missing fields
        if not fname or not bdate or not gender or not email:
            return jsonify({"error": "Missing required fields"}), 400

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbl_student (fname, bdate, gender, email) VALUES (?, ?, ?, ?)",
                       (fname, bdate, gender, email))
        conn.commit()
        return jsonify({"status": "success"}), 200

# Fetch individual student by id for API
@app.route('/api/students/<int:id>', methods=['GET'])
def api_student(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_student WHERE id = ?", (id,))
    student = cursor.fetchone()
    if student:
        student_dict = dict(student)
        return jsonify(student_dict)
    else:
        return jsonify({"error": "Student not found"}), 404

# DELETE individual student by id for API
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student_api(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbl_student WHERE id = ?", (id,))
    conn.commit()
    if cursor.rowcount > 0:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

# PUT route to update student information
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_student WHERE id = ?", (id,))
    student = cursor.fetchone()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    fname = data.get('fname')
    bdate = data.get('bdate')
    gender = data.get('gender')
    email = data.get('email')

    if not fname or not bdate or not gender or not email:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        cursor.execute("""
            UPDATE tbl_student
            SET fname = ?, bdate = ?, gender = ?, email = ?
            WHERE id = ?
        """, (fname, bdate, gender, email, id))
        conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to update student: {str(e)}"}), 500

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    fname = data.get('fname')
    bdate = data.get('bdate')
    gender = data.get('gender')
    email = data.get('email')

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbl_student (fname, bdate, gender, email) VALUES (?, ?, ?, ?)",
                   (fname, bdate, gender, email))
    conn.commit()
    return jsonify({"status": "success"}), 200

@app.route('/edit/<int:id>', methods=['GET', 'POST'], endpoint='edit')
def edit(id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Handle form submission to update student
        fname = request.form['fname']
        bdate = request.form['bdate']
        gender = request.form['gender']
        email = request.form['email']

        cursor.execute("""UPDATE tbl_student
                          SET fname = ?, bdate = ?, gender = ?, email = ?
                          WHERE id = ?""", (fname, bdate, gender, email, id))
        conn.commit()
        return redirect(url_for('index'))  # Redirect back to the student list

    # If GET request, show the current student data in the form
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

    now = datetime.now()
    return render_template('view.html', student=student, now=now)

if __name__ == '__main__':
    app.run(debug=True)

    
@app.route('/menu')
def menu():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_student")
    students = cursor.fetchall()

    return render_template('menu.html', students=students)

@app.route('/view_all_students')
def view_all_students():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_student")
    students = cursor.fetchall()

    # You can render this to show all students
    return render_template('index.html', students=students)




