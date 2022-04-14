from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.book import Book
from flask_app.models.author import Author


@app.route('/books')
def books():
    books = Book.get_all();
    return render_template('books.html', books=books)

@app.route('/create_book', methods=["POST"])
def create_book():
    data = {
        "title": request.form['title'],
        "num_of_pages":request.form['num_pages']
    }
    Book.save(data)
    return redirect('/books')

@app.route('/book/<book_id>')
def book(book_id):
    data = {"id":book_id}
    book_with_authors = Book.get_authors_by_book_id(data)

    #get books not faved by author
    all_authors = Author.get_all() #get all authors
    faved_authors = [] #two empty lists, one for the faved ones and one for the unfaved ones
    unfaved_authors = []
    for author in book_with_authors.authors: #add all faved authors to faved author list
        faved_authors.append(author.id)
    for author in all_authors: #compare faved list to all authors and save the ones that are NOT in the faved list to the unfaved list
        if author.id not in faved_authors:
            unfaved_authors.append(author)

    return render_template('book.html', book=book_with_authors, authors=book_with_authors.authors, unfaved_authors = unfaved_authors)

@app.route('/add_author', methods=["POST"])
def add_author():
    data = {
        "author_id": request.form["author_id"],
        "book_id": request.form["book_id"]
    }
    Book.add_author_to_faved(data)
    return redirect(f"/book/{request.form['book_id']}")