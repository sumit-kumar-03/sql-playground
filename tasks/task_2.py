from execute_sql import main


executor = main()


## DATA Generation, Manipukation and Conversion
## DATA Types :- CHAR, VARCHAR, AND TEXT


# Create table
query = """
CREATE TABLE string_tbl
(char_fld CHAR(30),
vchar_fld VARCHAR(30),
text_fld TEXT
)
"""


# String Generation
query = """
INSERT INTO string_tbl (char_fld, vchar_fld, text_fld)
VALUES ('this is char data', 'this is varchar data', 'this is text data');
"""


# Check limit
query = """
UPDATE string_tbl
SET vchar_fld = '***************************************************************************************************';
"""


# Check mode
query = """
SELECT @@session.sql_mode;
"""
# Columns: @@session.sql_mode
# [('ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION',)]



# Update mode 
query = """
SET sql_mode='ansi';
"""
## need to pass for every session


# Special character 
query = """
UPDATE string_tbl
SET text_fld = 'It won't work';
"""


# Use double slashes to escape things
query = """
UPDATE string_tbl
SET text_fld = 'Now it\\'s working with double slashes';
"""


query = """
SELECT *
FROM string_tbl;
"""


# Using safe quote function to fetch data
query = """
SELECT quote(text_fld)
FROM string_tbl;
"""


# Concatenate function
query = """
SELECT CONCAT('danke sch',CHAR(148),'n');
"""


# ASCII func
query = """
SELECT ASCII('b');
"""


## STRING Manipulation
# Delete
query = """
DELETE FROM string_tbl;
"""

query = """
SELECT *
FROM string_tbl;
"""

query = """
INSERT INTO string_tbl (char_fld, vchar_fld, text_fld)
VALUES ('this is char data', 'this is varchar data', 'this is text data');
"""

# Length
query = """
SELECT LENGTH(char_fld) char_len, LENGTH(vchar_fld) vchar_len, LENGTH(text_fld) text_len
FROM string_tbl;"""

# Find position (1st occurance) position starts with 1, if 0 then not found
query = """
SELECT POSITION('text' IN text_fld)
FROM string_tbl;"""

# locate it has 3 positional args 3rd to start the search from which position
query = """
SELECT LOCATE('is', text_fld, 5)
FROM string_tbl;"""


# string comparisons
query = """
SELECT STRCMP('12345','12345') 12345_12345,
STRCMP('abcd','xyz') abcd_xyz,
STRCMP('abcd','QRSTUV') abcd_QRSTUV,
STRCMP('qrstuv','QRSTUV') qrstuv_QRSTUV,
STRCMP('12345','xyz') 12345_xyz,
STRCMP('xyz','qrstuv') xyz_qrstuv;
"""


# 
query = """
UPDATE string_tbl
SET text_fld = CONCAT('- START -',text_fld, '- EXTRA -');
"""

query = """
SELECT *
FROM string_tbl;
"""


# Exercise 7-1
# Write a query that returns the 17th through 25th characters of the string 'Please
# find the substring in this string'.
query = """
SELECT SUBSTRING('Please find the substring in this string', 17, 25);"""

# Exercise 7-2
# Write a query that returns the absolute value and sign (−1, 0, or 1) of the number
# −25.76823. Also return the number rounded to the nearest hundredth.
query = """
SELECT SIGN(-25.76823);
"""

# Exercise 7-3
# Write a query to return just the month portion of the current date.
query = """
SELECT EXTRACT(YEAR FROM CURRENT_DATE());
"""


# Grouping Concepts
query = """
SELECT customer_id, count(*)
FROM rental
GROUP BY customer_id
ORDER BY count(*) DESC 
LIMIT 5;
""" 


# having filter
query = """
SELECT customer_id, count(*)
FROM rental
GROUP BY customer_id
HAVING count(*)>=40
ORDER BY 2 DESC;
"""


# Aggregate Function
query = """
SELECT MAX(amount) max_amt,
MIN(amount) min_amt,
AVG(amount) avg_amt,
SUM(amount) ttl_amt,
COUNT(*) num_payments
FROM payment;
"""


# Aggregate Function with group by
query = """
SELECT customer_id,
MAX(amount) max_amt,
MIN(amount) min_amt,
AVG(amount) avg_amt,
SUM(amount) ttl_amt,
COUNT(*) num_payments
FROM payment
GROUP BY customer_id
ORDER BY ttl_amt
LIMIT 5;
"""


# Use of distint 
query = """
SELECT COUNT(customer_id) num_rows,
COUNT(DISTINCT customer_id) num_cust
FROM payment;
"""

# Use Expressions
query = """
SELECT MAX(datediff(return_date,rental_date))
FROM rental;
"""

# lets discuss NULL
query = """
SELECT customer_id, rental_id, return_date
FROM rental
WHERE return_date IS NULL
LIMIT 5;
"""

query = """
SELECT customer_id, rental_id, return_date
FROM rental
WHERE return_date IS NOT NULL
LIMIT 5;
"""



## Grouping and Aggregates 
# Group by
query = """
SELECT customer_id, count(rental_id) AS rented
FROM rental
GROUP BY customer_id
ORDER BY rented DESC
LIMIT 5;
"""

# Filter condition 
query = """
SELECT customer_id, count(*) AS rented
FROM rental
GROUP BY customer_id 
HAVING rented >= 40;
"""

# Aggregates
query = """
SELECT MAX(amount) max_amt,
MIN(amount) min_amt,
AVG(amount) avg_amt,
SUM(amount) ttl_amt,
COUNT(*) num_payments
FROM payment;
"""

# Aggregrate on derived table
query ="""
SELECT MAX(rent_num) AS max_num,
MIN(rent_num) AS min_num,
AVG(rent_num) AS avg_num,
SUM(rent_num) AS ttl_num,
COUNT(rent_num) AS ttl_renters
FROM (
SELECT customer_id, count(rental_id) AS rent_num
FROM rental
GROUP BY customer_id) as t;"""


# Aggregrate on group by field
query = """
SELECT customer_id AS CUST,
MAX(amount) AS max_amt,
MIN(amount) AS min_amt,
AVG(amount) AS avg_amt,
SUM(amount) AS ttl_amt,
COUNT(*) AS ttl_num_amt
FROM payment
GROUP BY customer_id
ORDER BY ttl_num_amt DESC
LIMIT 5;
"""


# LIKE operator
query ="""
SELECT name AS NAME, 
name LIKE 'a%' AS starts_with_a,
name LIKE '%y' AS ends_with_y,
name LIKE '%a%' AS contains_a
FROM category; 
"""


# Regex
query ="""
SELECT name AS NAME,
name REGEXP '^a' AS starts_with_a,
name REGEXP 'y$' AS ends_with_y,
name REGEXP '.*a.*' AS contains_a
FROM category;
"""


# Concatenation 
query ="""
SELECT concat('hi',', how',' are', ' you') AS sentance;
"""


# Insert :--> INSERT(string_to_insert_in, position_of_insertion, number_of_object_to_be_replaced, obj_to_be_inserted)
query ="""
SELECT INSERT('sm',2,0,'a') AS name;
"""


query ="""
SELECT INSERT('suuit',3,1,'m') AS name;
"""


# Substring 
query = """
SELECT SUBSTRING('sumit', 3, 1) AS sub;
"""


# Replace
query = """
SELECT REPLACE('sumit sam', 'sam', 'kumar') as rep;
"""


# 

# Execute query
results = executor.execute_query(query)


print(results)
executor.close()