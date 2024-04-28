import sqlite3
from models import Book

def get_all_books():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
        """
        SELECT
            a.id,
            a.title,
            a.image,
            a.price,
            a.sale,
            a.description
        FROM Books a
        """)

        books = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            book = Book(row['id'], row['title'], row['image'], row['price'], row['sale'], row['description'] )
            books.append(book.__dict__)

        return books
    
def get_single_book(id):
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
        FROM Books a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        book = Book(data['id'], data['email'], data['first_name'],
                            data['last_name'], data['image'],
                            data['favorite'])

        return book.__dict__
    
    
def create_book(new_book):
    # title, image, price, sale, description
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Books
            ( title, image, price, sale, description )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_book['title'],
              new_book['image'], new_book['price'],
              new_book['sale'], new_book['description'], ))
        
        id = db_cursor.lastrowid
        new_book['id'] = id
        return new_book
    
def update_books(id, new_book):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Books
            SET
                first_name = ?,
                last_name = ?,
                image = ?,
                favorite = ?
        WHERE id = ?
        """, (new_book['first_name'], new_book['last_name'],
              new_book['image'], new_book['favorite'],
             id, ))
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
    
def delete_books(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Books
        WHERE id = ?
        """, (id, ))
    