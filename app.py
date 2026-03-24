from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home (Read + Lock Logic)
@app.route('/')
def home():
    conn = get_db_connection()
    capsules = conn.execute('SELECT * FROM capsules').fetchall()
    conn.close()

    current_date = date.today().isoformat()
    return render_template('index.html', capsules=capsules, current_date=current_date)

# Create
@app.route('/add', methods=['POST'])
def add():
    message = request.form['message']
    date_value = request.form['date']

    conn = get_db_connection()
    conn.execute('INSERT INTO capsules (message, date) VALUES (?, ?)', (message, date_value))
    conn.commit()
    conn.close()

    return redirect('/?success=1')

# Delete
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM capsules WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect('/')

# Update (Edit)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    capsule = conn.execute('SELECT * FROM capsules WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        message = request.form['message']
        date_value = request.form['date']

        conn.execute(
            'UPDATE capsules SET message = ?, date = ? WHERE id = ?',
            (message, date_value, id)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    conn.close()
    return render_template('edit.html', capsule=capsule)

@app.route('/view-data')
def view_data():
    conn = get_db_connection()
    capsules = conn.execute('SELECT * FROM capsules').fetchall()
    conn.close()

    return render_template('view.html', capsules=capsules)

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)