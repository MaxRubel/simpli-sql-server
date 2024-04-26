import sqlite3
from models import Author

def get_all_authors():
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
    # def __init__(self, id, email, first_name, last_name, image, favorite):
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

        authors = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            author = Author(row['id'], row['email'], row['first_name'], row['last_name'], row['image'], row['favorite'] )
            authors.append(author.__dict__)

        return authors
    
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
    