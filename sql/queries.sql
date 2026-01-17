SELECT * 
FROM products;

SELECT *
FROM products
WHERE price > 50000;

SELECT fk_product_id, amount
FROM bill_details
WHERE fk_product_id = 3456;

SELECT fk_product_id,
SUM(amount) as total_amount
FROM bill_details
GROUP BY fk_product_id;

SELECT *
FROM bills
WHERE email_customers = 'hjejh34@gmail.com';

SELECT *
FROM bills
ORDER BY total_amount DESC;

SELECT *
FROM bills
WHERE pk_id_bill = 335455;
