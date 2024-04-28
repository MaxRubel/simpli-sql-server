-- CREATE TABLE Authors (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     email TEXT,
--     first_name TEXT,
--     last_name TEXT,
--     image TEXT,
--     favorite BOOLEAN
-- );

-- Drop table Author;

-- INSERT INTO Authors (email, first_name, last_name, image, favorite)
-- VALUES (
--     'barack@whitehouse.com',
--     'Barack',
--     'Obama',
--     'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/1280px-President_Barack_Obama.jpg',
--     0
-- );

-- DROP table book;

-- SELECT
--     a.email,
--     a.first_name,
--     a.last_name,
--     a.image,
--     a.favorite
-- FROM a Authors;

-- CREATE TABLE Books (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   title TEXT,
--   image TEXT,
--   price DECIMAL(10, 2),
--   sale BOOLEAN,
--   description TEXT
-- );

CREATE TABLE Author_Books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER,
  book_id INTEGER,
  FOREIGN KEY (author_id) REFERENCES Authors(id),
  FOREIGN KEY (book_id) REFERENCES Books(id)
);

-- INSERT INTO 'Book' VALUES (
-- null,
-- 'A Promised Land',
-- 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.penguinrandomhouse.com%2Fbooks%2F562882%2Fa-promised-land-by-barack-obama%2F&psig=AOvVaw3avAF9EylCGeBfo8Rt3atX&ust=1714248813035000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLDsqM7Y4IUDFQAAAAAdAAAAABAE',
-- '69.00',
-- FALSE,
-- 'A book by Barak Obama'
-- );


-- INSERT INTO `Employee` VALUES (null, "Madi Peper", "35498 Madison Ave", 1);