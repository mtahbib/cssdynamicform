from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'employee_data'

mysql = MySQL(app)

@app.route('/')
def index():
    # Fetch and display existing employee data
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, name, emp_id, designation FROM employees')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', employees=data)

@app.route('/add', methods=['POST'])
def add_employee():
    # Add new employee data to the database
    if request.method == 'POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        designation = request.form['designation']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO employees (name, emp_id, designation) VALUES (%s, %s, %s)', (name, emp_id, designation))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_employee(id):
    # Update employee data in the database
    if request.method == 'POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        designation = request.form['designation']

        cur = mysql.connection.cursor()
        cur.execute('UPDATE employees SET name=%s, emp_id=%s, designation=%s WHERE id=%s', (name, emp_id, designation, id))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_employee(id):
    # Delete employee data from the database
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM employees WHERE id=%s', (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
