import sqlite3
from models import Book, Author

def get_all_books():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        #get books
        db_cursor.execute(
        """
        SELECT
        *
        FROM Books a
        """)

        books = []
        dataset = db_cursor.fetchall()
        
        #get author_ids of book
        for row in dataset:
            book = Book(row['id'], row['title'], row['image'], row['price'], row['sale'], row['description'] )
            db_cursor.execute(
            """
            SELECT
            a.author_id
            FROM author_books a
            WHERE book_id = ?
            """, (book.id,))
            
            dataset2 = db_cursor.fetchall()
            author_ids = []
            
            #get author_info of book
            for row in dataset2:
                author_ids.append(row['author_id'])
                
            #book with no author gets inserted into list still:
            if len(author_ids) == 0:
                books.append(book.__dict__)
            for author_id in author_ids:
                db_cursor.execute(
                """
                SELECT
                *
                FROM Authors
                WHERE id = ?
                """, (author_id,))
                dataset3 = db_cursor.fetchall()
                authors = []
                for row in dataset3:
                    author = Author(row['id'], row['email'], row['first_name'], row['last_name'], row['image'], row['favorite'])
                    del author.books
                    author = author.__dict__
                    authors.append(author)
                book_dict = {
                'id': book.id,
                'title': book.title,
                'image': book.image,
                'price': book.price,
                'sale': book.sale,
                'description': book.description,
                'authors': authors
                }
   
                books.append(book_dict)

        return books
    
def get_single_book(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            b.id,
            b.title,
            b.image,
            b.price,
            b.sale,
            b.description
        FROM Books b
        WHERE b.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        book = Book(data['id'], data['title'], data['image'], data['price'], data['sale'], data['description'])
        author_ids = []
        authors = [] 
        db_cursor.execute("""
            SELECT
            a. author_id
            FROM author_books a
            WHERE a.book_id = ?
            """, ( id, ))
        dataset = db_cursor.fetchall()

        for row in dataset:
            author_id = row['author_id']
            author_ids.append(author_id)
            
        for author_id in author_ids:
            db_cursor.execute("""
            SELECT
            *
            FROM authors
            WHERE id = ?
            """, ( author_id, ))  
            dataset=db_cursor.fetchall()
            
            for row in dataset:
                author = Author(row['id'], row['email'], row['first_name'], row['last_name'], row['image'], row['favorite'])
                authors.append(author.__dict__)
                
        book = book.__dict__
        book['authors'] = authors
        return book
    
    
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
    
def update_book(id, new_book):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Books
            SET
                title = ?,
                image = ?,
                price = ?,
                sale = ?,
                description = ?
        WHERE id = ?
        """, (new_book['title'], new_book['image'],
              new_book['price'], new_book['sale'],new_book['description'],
             id, ))
        rows_affected = db_cursor.rowcount
        #get author_book
        db_cursor.execute("""
        DELETE FROM author_books
        WHERE book_id = ?
        """, (id, ))
        
        dataset = db_cursor.fetchall()

    # return value of this function
    if rows_affected == 0:
        return False
    else:
        return True
    
def delete_book(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM Books
        WHERE id = ?
        """, (id, ))
        db_cursor.execute("""
        DELETE FROM Author_Books
        WHERE book_id = ?
        """, (id, ))
    