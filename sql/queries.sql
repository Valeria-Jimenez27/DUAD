SELECT * 
FROM products;

SELECT *
FROM products
WHERE price > 50000;

SELECT *
FROM bill_details
WHERE pk_detail_id= 335455;

SELECT 
    fk_product_id,
    SUM(amount) as total_amount
FROM bill_details
GROUP BY fk_product_id;

SELECT *
FROM bill_details
WHERE pk_detail_id = 2;

SELECT *
FROM bills
ORDER BY total_amount DESC;

SELECT *
FROM bills
WHERE pk_id_bill = 335455;
