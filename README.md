# Student Management System

A full-stack web application for managing student records,
built with Python Flask and MySQL.

## Features
- Add new student records
- View all students in a table
- Edit existing student details
- Delete student records
- Search students by name or course
- Form validation with error messages
- Flash notifications for all actions

## Technologies Used
| Layer | Technology |
|---|---|
| Frontend | HTML, CSS |
| Backend | Python, Flask |
| Database | MySQL |
| Connector | PyMySQL |

## Project Structure

student_management/
├── app.py              # Flask backend
├── templates/          # HTML pages
│   ├── index.html
│   ├── add_student.html
│   ├── edit_student.html
│   └── search.html
├── static/
│   └── style.css       # Styling
├── .gitignore
└── README.md


## Setup Instructions

### 1. Install Python 3.11+
Download from https://python.org

### 2. Install required packages
```bash
python -m pip install flask pymysql cryptography
```

### 3. Setup MySQL Database
```sql
CREATE DATABASE student_management;
USE student_management;
CREATE TABLE students (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    age        INT NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    phone      VARCHAR(15),
    course     VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Update database password in app.py
```python
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",  # change this
        database="student_management"
    )
```

### 5. Run the application
```bash
python app.py
```

### 6. Open in browser
http://127.0.0.1:5000/



## What I Learned
- 3-tier architecture (Frontend + Backend + Database)
- Full CRUD operations
- SQL database design
- Flask routing and templating
- Form validation (frontend + backend)
- Connecting Python to MySQL

## Author
Satyajit Mirdda — satyajitMCA