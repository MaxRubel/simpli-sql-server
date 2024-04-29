import sqlite3
from models import Author, Book

def get_all_authors():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute(
        """
        SELECT
            a.id,
            a.email,
            a.first_name,
            a.last_name,
            a.image,
            a.favorite
        FROM Authors a
        """)
        dataset = db_cursor.fetchall()
        authors = []
        for row in dataset:
            author = Author(row['id'], row['email'], row['first_name'], row['last_name'], row['image'], row['favorite'] )
            authors.append(author.__dict__)

        for author in authors:
            # get author_books
            db_cursor.execute(
            """
            SELECT 
            a.book_id 
            FROM author_books a
            WHERE author_id = ?
            """, (author['id'], ))
            
            dataset = db_cursor.fetchall()
            book_ids = []
            books = []
            for row in dataset:
                book_ids.append(row['book_id'])
            # get books
            for id in book_ids:
                db_cursor.execute(
                """
                SELECT 
                * 
                FROM Books
                WHERE id = ?
                """, (id, ))  
                dataset = db_cursor.fetchall()
                #pacakge each book
                for row in dataset:
                    book = Book(row['id'],row['title'], row['image'], row['price'], row['sale'], row['description'])
                    books.append(book.__dict__)   
            # add books list to author
            author['books'] = books
                    
        return authors
    
def get_single_author(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.email,
            a.first_name,
            a.last_name,
            a.image,
            a.favorite
        FROM Authors a
        WHERE a.id = ?
        """, ( id, ))
        data = db_cursor.fetchone()
        author = Author(data['id'], data['email'], data['first_name'], data['last_name'], data['image'],
        data['favorite'])
        author = author.__dict__
        # get author books
        db_cursor.execute("""
        SELECT
        a.book_id
        FROM Author_books a
        WHERE a.author_id = ?
        """, ( id, ))
        dataset = db_cursor.fetchall()
        book_ids = []
        books = []
        
        for row in dataset:
            book_ids.append(row['book_id'])

        for book_id in book_ids:
            db_cursor.execute("""
            SELECT
            *
            FROM Books
            WHERE id = ?
            """, ( book_id, ))
            data = db_cursor.fetchone()
            book = Book(data['id'], data['title'], data['image'], data['price'], data['sale'], data['description'])
            books.append(book.__dict__)
            
        
        author['books'] = books
        return author

def create_author(new_author):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
            # def __init__(self, id, email, first_name, last_name, image, favorite):
        db_cursor.execute("""
        INSERT INTO Authors
            ( email, first_name, last_name, image, favorite )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_author['email'],
              new_author['first_name'], new_author['last_name'],
              new_author['image'], new_author['favorite'], ))
        
        id = db_cursor.lastrowid
        new_author['id'] = id
        return new_author
    
def update_author(id, new_author):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Authors
            SET
                first_name = ?,
                last_name = ?,
                image = ?,
                favorite = ?
        WHERE id = ?
        """, (new_author['first_name'], new_author['last_name'],
              new_author['image'], new_author['favorite'],
             id, ))
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        return False
    else:
        return True
    
def delete_author(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Authors
        WHERE id = ?
        """, (id, ))
        db_cursor.execute("""
        DELETE FROM Author_books
        WHERE author_id = ?
        """, (id, ))
    