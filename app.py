from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    capsules = conn.execute('SELECT * FROM capsules').fetchall()
    conn.close()
    return render_template('index.html', capsules=capsules)

@app.route('/add', methods=['POST'])
def add():
    message = request.form['message']
    date = request.form['date']

    conn = get_db_connection()
    conn.execute('INSERT INTO capsules (message, date) VALUES (?, ?)', (message, date))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM capsules WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)