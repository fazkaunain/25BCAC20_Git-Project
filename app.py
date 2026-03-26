from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "secret123"


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# -------- REGISTER --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        existing = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        if existing:
            error = "❌ Username already exists"
        else:
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect('/login')

        conn.close()

    return render_template('register.html', error=error)


# -------- LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/')
        else:
            error = "❌ Invalid username or password"

    return render_template('login.html', error=error)


# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# -------- HOME --------
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    capsules = conn.execute(
        'SELECT * FROM capsules WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    current_date = date.today().isoformat()

    return render_template(
        'index.html',
        capsules=capsules,
        current_date=current_date,
        username=session.get('username')
    )


# -------- ADD --------
@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/login')

    message = request.form['message']
    date_value = request.form['date']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO capsules (user_id, message, date) VALUES (?, ?, ?)',
        (session['user_id'], message, date_value)
    )
    conn.commit()
    conn.close()

    return redirect('/?success=1')


# -------- DELETE --------
@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    conn.execute(
        'DELETE FROM capsules WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    )
    conn.commit()
    conn.close()

    return redirect('/?deleted=1')


# -------- EDIT --------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()

    capsule = conn.execute(
        'SELECT * FROM capsules WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    ).fetchone()

    if capsule is None:
        conn.close()
        return "Unauthorized access!"

    if request.method == 'POST':
        message = request.form['message']
        date_value = request.form['date']

        conn.execute(
            'UPDATE capsules SET message = ?, date = ? WHERE id = ?',
            (message, date_value, id)
        )
        conn.commit()
        conn.close()

        return redirect('/?success=1')

    conn.close()
    return render_template('edit.html', capsule=capsule)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)