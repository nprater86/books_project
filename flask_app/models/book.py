# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author
# model the class after the table from our database
class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM books ORDER BY title;'
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('books_schema').query_db(query)
        # Create an empty list to append our instances of table
        books = []
        # Iterate over the db results and create instances of table with cls.
        for book_row in results:
            books.append( cls(book_row) )
        return books

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO books (title, num_of_pages, created_at, updated_at) VALUES (%(title)s,%(num_of_pages)s,NOW(),NOW());'
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE books SET title = %(title)s, updated_at = NOW() WHERE id = %(id)s;'
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM books WHERE id = %(id)s;'
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_book_by_id(cls, data):
        query = 'SELECT * FROM books WHERE id = %(id)s;'
        results = connectToMySQL('books_schema').query_db(query, data)
        target_book = results[0]
        return target_book

    @classmethod
    def get_authors_by_book_id(cls, data):
        query = 'SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;'
        results = connectToMySQL('books_schema').query_db(query, data)
        book = cls( results[0] )
        for author_row in results:
            author_data = {
                "id": author_row["authors.id"],
                "first_name": author_row["first_name"],
                "last_name": author_row["last_name"],
                "created_at": author_row["authors.created_at"],
                "updated_at": author_row["authors.updated_at"]
            }
            book.authors.append( author.Author(author_data) )
        return book

    @classmethod
    def add_author_to_faved(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)