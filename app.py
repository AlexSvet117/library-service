from flask import Flask, jsonify, render_template

app = Flask(__name__)

# list of books
books = [
    {"book_id": "001", "title":"Pete the Cat and Cupcakes", "author": "Some Dude", "publication_year": 2005, 
     "genre":"Kids books", "read_status":"read", "rating": 5.0, "notes":"Great book for bed reading"},
    {"book_id": "002", "title":"Oi Dog", "author": "Some Other Dude", "publication_year": 2011, 
     "genre":"Kids books", "read_status":"reading", "rating": 4.8, "notes":"Very funny book. Lots of humor."},
    {"book_id": "003", "title":"Oi Aardvark", "author": "Some Other Dude", "publication_year": 2012, 
     "genre":"Kids books", "read_status":"reading", "rating": 4.7, "notes":"Great book. Very funny story."},
    {"book_id": "004", "title":"Giraffe can't Dance", "author": "Some Crazy Dude", "publication_year": 2000, 
     "genre":"Kids books", "read_status":"read", "rating": 5.0, "notes":"Great book! Awesome!"},
    {"book_id": "005", "title":"Unicorns don't wear Tutu", "author": "Some Dude", "publication_year": 2007, 
     "genre":"Kids books", "read_status":"to-read", "rating": 0.0, "notes":"To be read, but should be also very interesting and funny"}
]


@app.route("/")
def home():
    return render_template("index.html")


# returns all the books from the list of books
@app.route("/api/books", methods = ["GET"])
def get_all_books():
    return jsonify(books)

# returns selected book
@app.route("/api/books/<string:book_id>")
def get_selected_book(book_id):
    for book in books:
        if book_id == book.get("book_id"):
            return jsonify(book), 200
    return jsonify({"error" :f"The book with book id {book_id} is not found"}), 404



if __name__ == "__main__":
    app.run(debug=True)
