from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def authors():
    authors = Author.get_all();
    return render_template('authors.html', authors=authors)

@app.route('/author/<author_id>')
def author(author_id):
    data = {"id":author_id}
    target_author = Author.get_author_by_id(data)
    author = Author.get_books_by_author_id(data)

    #get books not faved by author
    all_books = Book.get_all()
    faved_books = []
    unfaved_books = []
    for book in author.books:
        faved_books.append(book.id)
    for book in all_books:
        if book.id not in faved_books:
            unfaved_books.append(book)

    return render_template('author.html',author=target_author, books=author.books, unfaved_books = unfaved_books)

@app.route('/create_author', methods=["POST"])
def create_author():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name']
    }
    Author.save(data)
    return redirect('/authors')

@app.route('/add_favorite', methods=["POST"])
def add_favorite():
    data = {
        "author_id":request.form["author_id"],
        "book_id":request.form["book_id"]
    }
    Author.add_book_to_faves(data)
    return redirect(f"/author/{request.form['author_id']}")
