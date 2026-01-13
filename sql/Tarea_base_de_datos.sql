UPDATE bills
SET total_amount = CASE pk_id_bill
    WHEN 335455 THEN 150
END
WHERE pk_id_bill IN (335455);






