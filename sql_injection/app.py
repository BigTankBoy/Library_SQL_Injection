from flask import Flask, render_template, request, redirect, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = "s3cr3t_key"
DATABASE = 'blind_library_with_users.db'

# ----------------- DB HANDLING -----------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_conn(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ----------------- AUTH -----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        db = get_db()
        try:
            db.execute("INSERT INTO users(username,password) VALUES (?,?)", (u, p))
            db.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Username already taken", 400
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
        if user:
            session['uid'] = user['id']
            return redirect('/')
        return "Invalid", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ----------------- LIBRARY -----------------

@app.route('/')
def index():
    db = get_db()
    genres = db.execute('SELECT DISTINCT genre FROM books').fetchall()
    return render_template('index.html', genres=genres)

@app.route('/genre')
def genre():
    genre = request.args.get('genre')
    db = get_db()
    books = db.execute('SELECT * FROM books WHERE genre=?', (genre,)).fetchall()
    return render_template('genre.html', genre=genre, books=books)

@app.route('/book/<int:bid>')
def book(bid):
    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id=?', (bid,)).fetchone()
    return render_template('book.html', book=book)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    db = get_db()
    # Intentionally vulnerable SQL
    sql = f"SELECT id,genre,title,author,content FROM books WHERE title LIKE '%{q}%'"
    rows = []
    try:
        rows = db.execute(sql).fetchall()
    except sqlite3.Error:
        pass
    return render_template('search.html', rows=rows, q=q)

if __name__ == '__main__':
    app.run(debug=True)