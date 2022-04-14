# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book
# model the class after the table from our database
class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM authors;'
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('books_schema').query_db(query)
        # Create an empty list to append our instances of table
        authors = []
        # Iterate over the db results and create instances of table with cls.
        for author_row in results:
            authors.append( cls(author_row) )
        return authors

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO authors (first_name, last_name, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,NOW(),NOW());'
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE authors SET first_name = %(first_name)s, last_name = %(last_name)s, dojo_id = %(dojo_id)s WHERE id = %(id)s;'
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM authors WHERE id = %(id)s;'
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_books_by_author_id(cls, data):
        query = 'SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;'
        results = results = connectToMySQL('books_schema').query_db(query, data)
        author = cls( results[0] )
        for book_row in results:
            book_data = {
                "id": book_row['books.id'],
                "title": book_row['title'],
                "num_of_pages": book_row['num_of_pages'],
                "created_at": book_row['books.created_at'],
                "updated_at": book_row['books.updated_at']
            }
            author.books.append(book.Book(book_data))
        return author

    @classmethod
    def get_author_by_id(cls, data):
        query = 'SELECT * FROM authors WHERE id = %(id)s;'
        results = connectToMySQL('books_schema').query_db(query, data)
        target_author = results[0]
        return target_author

    @classmethod
    def add_book_to_faves(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)
