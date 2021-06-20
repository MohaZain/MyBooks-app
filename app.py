from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
# import psycopg2

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Book(db.Model):
    __tablename__= "books"
    
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(180), nullable=False)
    authorName = db.Column(db.String(80), nullable=False)
    bookType = db.Column(db.String(40), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
# TODO: implment a GET request to fetch all books
@app.route('/')
def index():
    book = Book.query.all()
    return render_template('my-books.html', books=book)

@app.route('/add-book')
def addBook():
    
    return render_template('add-book.html')

# TODO: implment a POST request of adding a book 
@app.route('/add-book/create', methods=['POST'])
def createBook():
    error = False
    body = {}
    try:
        title = request.get_json()["title"]
        author = request.get_json()["author"]
        type = request.get_json()["type"]
        book = Book(bookTitle=title, authorName=author,bookType=type)
        db.session.add(book)
        db.session.commit()
        # body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return render_template('my-books.html') 

# TODO: implment a PUT request to mark the book as read
@app.route('/read/<bookId>', methods = ['PUT'])
def read_book(bookId):
    try:
        read = Book.query.get(bookId)
        read.completed = True
        db.session.add(read)
        db.session.commit()
    except:
        print(sys.exc_info())
    finally:
        db.session.close()
    return render_template('my-books.html')

# TODO: implment a Delete request to delete a book
@app.route('/delete/<bookId>', methods = ['GET'])
def delete_book(bookId):
    try:
        Book.query.filter_by(id=bookId).delete()
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return render_template('my-books.html')

# Default port:
if __name__ == '__main__':
    app.run(debug=True)