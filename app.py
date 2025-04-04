from flask import Flask, jsonify, render_template, request

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
     "genre":"Kids books", "read_status":"to-read", "rating": 4.6, "notes":"To be read, but should be also very interesting and funny"}
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/books", methods = ["GET"])
def get_all_books():
    """
    Functions used to return list of existing books
    """
    return jsonify(books)


@app.route("/api/books/<string:book_id>", methods = ["GET"])
def get_selected_book(book_id):
    """
    Function returns selected book based on provided book_id
    Functions returns error if book is not found
    """
    for book in books:
        if book_id == book.get("book_id"):
            return jsonify(book), 200
    return jsonify({"error" :f"The book with book id {book_id} is not found"}), 404


@app.route("/api/books", methods = ["POST"])
def add_book():
    """
    Functions adds a new book to the list of books
    User request body to add data
    Validates that data was submitted and returns error if payload is empty
    Validates if new_book is already in the list and returns error if book is already present
    Validates if the new_book and title are present in the submitted data and returns error otherwise

    Request body = 
    { "book_id": str *, 
    "title": str *, 
    "author": str, 
    "publication_year": int, 
    "genre": str, 
    "read_status": str, 
    "rating": float, 
    "notes": str
    }
    """
    new_book = request.get_json()
    
    if not new_book:
        return jsonify({"error": "The payload can not be empty"}), 400
    if "book_id" not in new_book or "title" not in new_book:
        return jsonify({"error": "Fields book_id and title are requiered"}), 400
    
    for book in books:
        if new_book.get("book_id") == book.get("book_id"):
            return jsonify({"error": f"book_id {new_book.get("book_id")} is already present"}), 400
    
    books.append(new_book)
    return jsonify({"status" : f"Successfully added new book with book_id {new_book.get("book_id")}", "books": books}), 201


@app.route("/api/books/<string:book_id>", methods = ["PUT"])
def update_book(book_id):
    """
    Function updates a book if book exists in the list
    Functions uses book id to determine which book to update
    """
    book_to_update = None
    for book in books:
        if book_id == book.get("book_id"):
            book_to_update = book

    if book_to_update:
        new_book = request.json
        book_to_update.update(new_book)
        return jsonify({"status" : "Book successfully updated", "books" : books}), 201
    return jsonify({"error": "Book not found"}), 400


@app.route("/api/books/<string:book_id>", methods = ["DELETE"])
def delete_book(book_id):
    """
    Function for deletion of book if it is present in the list of books
    """
    book_delete = None
    for book in books:
        if book_id == book.get("book_id"):
            book_delete = book

    if book_delete:
        books.remove(book_delete)
        return jsonify({"status" : "Successfully deleted selected book", "books" : books}), 204
    return jsonify({"error": "The book not in the list"}), 400


@app.route("/api/books/stats", methods = ["GET"])
def books_stats():
    """
    Functions returns statistics of existing list of books
    - Total number of books in the library
    - Number of books by read status
    - Average rating across all books
    - Books count by genre
    """
    total_books = 0
    read = 0
    reading = 0
    to_read = 0
    total_raiting = 0.0
    av_raiting = 0.0
    genre_counts = {}

    for book in books:
        total_books = total_books + 1
        total_raiting = total_raiting + book.get("rating")

        genre = book.get("genre", "Unknown")
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

        if book.get("read_status") == "read":
            read = read + 1
        if book.get("read_status") == "to-read":
            to_read = to_read + 1
        if book.get("read_status") == "reading":
            reading = reading + 1
        
    if total_books > 0:
        av_raiting = total_raiting / total_books
    else:
        av_raiting = 0

    return jsonify({
        "status": "The stats are calculated", 
        "total_books": total_books,
        "read": read,
        "reading": reading,
        "to-read": to_read,
        "average_rating": av_raiting,
        "genre_counts": genre_counts
    }), 200



    

    





if __name__ == "__main__":
    app.run(debug=True)
