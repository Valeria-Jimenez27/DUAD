-- List all tables in the database
SELECT name FROM sqlite_master WHERE type='table';
-- Get the schema of the all tables
SELECT sql
FROM sqlite_master
WHERE type='table' AND name='products';

SELECT sql
FROM sqlite_master
WHERE type='table' AND name='bills';

SELECT sql
FROM sqlite_master
WHERE type='table' AND name='bill_details';

SELECT sql
FROM sqlite_master
WHERE type='table' AND name='shopping_cart';





