

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor
c = conn.cursor()

# Create employees table
c.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    salary REAL NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()
from flask import Flask, render_template, request, redirect, url_for # type: ignore
import sqlite3

app = Flask(_name_) # type: ignore

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=('GET', 'POST'))
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']

        conn = get_db_connection()
        conn.execute('INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)',
                     (name, position, salary))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_employee.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_employee(id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM employees WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']

        conn.execute('UPDATE employees SET name = ?, position = ?, salary = ? WHERE id = ?',
                     (name, position, salary, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_employee(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if _name_ == '_main_': # type: ignore
    app.run(debug=True)
    