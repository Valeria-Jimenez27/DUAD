SELECT authors.Name AS Author, books.Name AS Book
FROM Authors AS authors
INNER JOIN Books AS books
ON authors.ID = books.Author;

SELECT books.Name AS Book
FROM Books AS books
LEFT JOIN Authors AS authors
ON authors.ID = books.Author WHERE authors.ID IS NULL;

SELECT author.Name AS Author
FROM Authors AS author
LEFT JOIN Books AS books
ON books.Author = author.ID WHERE books.ID IS NULL;

SELECT DISTINCT books.Name
FROM Books AS books
INNER JOIN Rents AS rents
ON books.ID = rents.BookID;

SELECT Books.Name AS BookID
FROM Books AS Books
LEFT JOIN Rents AS Rents
ON Books.ID = Rents.BookID WHERE Rents.BookID IS NULL;

SELECT Customers.Name AS Customer
FROM Customers AS Customers
LEFT JOIN Rents AS Rents
ON Customers.ID = Rents.CustomerID WHERE Rents.CustomerID IS NULL;

SELECT DISTINCT books.Name AS Book
FROM Books AS books
INNER JOIN Rents AS rents
ON books.ID = rents.BookID WHERE rents.State = 'Overdue';
