from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import re

app = Flask(__name__)
app.secret_key = "student_management_secret"
# secret_key is required for flash messages to work

# --- Database Connection ---
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Ritesh987@#",
        database="student_management",
        cursorclass=pymysql.cursors.Cursor
    )

# --- Validation Function ---
def validate_student(name, age, email, phone, course):
    errors = []

    # Name validation
    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")
    elif len(name.strip()) > 100:
        errors.append("Name must be less than 100 characters.")
    elif not re.match(r"^[a-zA-Z\s]+$", name.strip()):
        errors.append("Name must contain letters only.")

    # Age validation
    if not age:
        errors.append("Age is required.")
    else:
        try:
            age_int = int(age)
            if age_int < 1 or age_int > 120:
                errors.append("Age must be between 1 and 120.")
        except ValueError:
            errors.append("Age must be a valid number.")

    # Email validation
    if not email or len(email.strip()) == 0:
        errors.append("Email is required.")
    elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email.strip()):
        errors.append("Please enter a valid email address.")

    # Phone validation (optional field)
    if phone and len(phone.strip()) > 0:
        if not re.match(r"^\d{10}$", phone.strip()):
            errors.append("Phone must be exactly 10 digits.")

    # Course validation
    if not course or len(course.strip()) < 2:
        errors.append("Course must be at least 2 characters.")
    elif len(course.strip()) > 100:
        errors.append("Course must be less than 100 characters.")

    return errors

# --- 1. Home ---
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    db.close()
    return render_template("index.html", students=students)

# --- 2. Add Student ---
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name   = request.form["name"].strip()
        age    = request.form["age"].strip()
        email  = request.form["email"].strip()
        phone  = request.form["phone"].strip()
        course = request.form["course"].strip()

        # Run validation
        errors = validate_student(name, age, email, phone, course)

        # Check for duplicate email
        if not errors:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT id FROM students WHERE email=%s", (email,)
            )
            if cursor.fetchone():
                errors.append("This email is already registered.")
            db.close()

        # If errors exist — show form again with errors
        if errors:
            return render_template(
                "add_student.html",
                errors=errors,
                form_data=request.form
            )

        # No errors — save to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, email, phone, course) "
            "VALUES (%s, %s, %s, %s, %s)",
            (name, age, email, phone, course)
        )
        db.commit()
        db.close()
        flash("Student added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add_student.html", errors=[], form_data={})

# --- 3. Edit Student ---
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        name   = request.form["name"].strip()
        age    = request.form["age"].strip()
        email  = request.form["email"].strip()
        phone  = request.form["phone"].strip()
        course = request.form["course"].strip()

        # Run validation
        errors = validate_student(name, age, email, phone, course)

        # Check duplicate email — exclude current student
        if not errors:
            cursor.execute(
                "SELECT id FROM students WHERE email=%s AND id!=%s",
                (email, id)
            )
            if cursor.fetchone():
                errors.append("This email is already used by another student.")

        if errors:
            cursor.execute(
                "SELECT * FROM students WHERE id=%s", (id,)
            )
            student = cursor.fetchone()
            db.close()
            return render_template(
                "edit_student.html",
                errors=errors,
                student=student,
                form_data=request.form
            )

        cursor.execute(
            "UPDATE students SET name=%s, age=%s, email=%s, "
            "phone=%s, course=%s WHERE id=%s",
            (name, age, email, phone, course, id)
        )
        db.commit()
        db.close()
        flash("Student updated successfully!", "success")
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    db.close()
    return render_template(
        "edit_student.html",
        errors=[],
        student=student,
        form_data={}
    )

# --- 4. Delete Student ---
@app.route("/delete/<int:id>")
def delete_student(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    db.close()
    flash("Student deleted successfully!", "danger")
    return redirect(url_for("index"))

# --- 5. Search ---
@app.route("/search")
def search():
    query = request.args.get("q", "")
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE name LIKE %s OR course LIKE %s",
        (f"%{query}%", f"%{query}%")
    )
    results = cursor.fetchall()
    db.close()
    return render_template(
        "search.html", students=results, query=query
    )

if __name__ == "__main__":
    app.run(debug=True)