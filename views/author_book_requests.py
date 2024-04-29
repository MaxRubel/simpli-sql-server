import sqlite3

def create_author_book(new_author_book):

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Author_Books
            ( author_id, book_id)
        VALUES
            ( ?, ?);
        """, (new_author_book['author_id'],
              new_author_book['book_id'],))
        
        id = db_cursor.lastrowid
        new_author_book['id'] = id
        return new_author_book