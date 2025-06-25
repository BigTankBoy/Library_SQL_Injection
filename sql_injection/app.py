from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
DATABASE = 'blind_library.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    genres = db.execute('SELECT DISTINCT genre FROM books').fetchall()
    return render_template('index.html', genres=genres)

@app.route('/genre')
def genre():
    genre = request.args.get('genre')
    db = get_db()
    books = db.execute('SELECT * FROM books WHERE genre = ?', (genre,)).fetchall()
    return render_template('genre.html', genre=genre, books=books)

@app.route('/book/<int:book_id>')
def book(book_id):
    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    return render_template('book.html', book=book)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    db = get_db()

    sql = f"SELECT * FROM books WHERE title LIKE '%{query}%'"
    books = []
    try:
        books = db.execute(sql).fetchall()
    except:
        pass

    return render_template('search.html', books=books, query=query)

if __name__ == '__main__':
    app.run(debug=True)