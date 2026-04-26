from execute_sql import main


executor = main()


###############
# learning sql by alan beaulieu - Chapter - 10
###############



# Query 1: Count number of copies per film using an inner join
query = """
SELECT f.film_id, f.title, count(*) num_copies
FROM film f
INNER JOIN inventory i
ON f.film_id = i.film_id
GROUP BY f.film_id
LIMIT 20; 
"""



# Query 2: Count number of copies per film using a left outer join (includes films with zero copies)
query = """
SELECT f.film_id, f.title, count(i.inventory_id) num_copies
FROM film f
LEFT OUTER JOIN inventory i
ON f.film_id = i.film_id
GROUP BY f.film_id
LIMIT 20; 
"""



# Query 3: Count number of copies per film using a right outer join
query = """
SELECT f.film_id, f.title, count(i.inventory_id) num_copies
FROM inventory i 
RIGHT OUTER JOIN film f
ON f.film_id = i.film_id
GROUP BY f.film_id
LIMIT 20; 
"""



# Query 4: Retrieve film details with inventory IDs and rental dates for films with IDs between 13 and 15
query = """
SELECT f.film_id, f.title, i.inventory_id, date(r.rental_date)
FROM film f
LEFT OUTER JOIN inventory i
ON f.film_id = i.film_id
LEFT OUTER JOIN rental r
ON r.inventory_id = r.inventory_id
WHERE f.film_id BETWEEN 13 AND 15
LIMIT 20;
"""



# Query 5: Generate a Cartesian product of categories and languages using a cross join (limited to 10 rows)
query = """
SELECT c.name category_name, l.name language_name
FROM category c
CROSS JOIN language l
LIMIT 10;
"""



# Query 6: Generate numbers 0-999 using cross join of digit tables
query = """
SELECT ones.num + tens.num + hundreds.num AS _number
FROM 
(
SELECT 0 num UNION ALL
SELECT 1 num UNION ALL
SELECT 2 num UNION ALL
SELECT 3 num UNION ALL
SELECT 4 num UNION ALL
SELECT 5 num UNION ALL
SELECT 6 num UNION ALL
SELECT 7 num UNION ALL
SELECT 8 num UNION ALL
SELECT 9 num
) ones
CROSS JOIN
(
SELECT 0 num UNION ALL
SELECT 10 num UNION ALL
SELECT 20 num UNION ALL
SELECT 30 num UNION ALL
SELECT 40 num UNION ALL
SELECT 50 num UNION ALL
SELECT 60 num UNION ALL
SELECT 70 num UNION ALL
SELECT 80 num UNION ALL
SELECT 90 num
) tens
CROSS JOIN
(
SELECT 0 num UNION ALL
SELECT 100 num UNION ALL
SELECT 200 num UNION ALL
SELECT 300 num
) hundreds
ORDER BY _number DESC
LIMIT 10;
"""




# Query 7: Generate dates from 2020-01-01 up to 2021-01-01 using cross join of digit tables
query = """
SELECT DATE_ADD('2020-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) dt
FROM 
(
SELECT 0 num UNION ALL
SELECT 1 num UNION ALL
SELECT 2 num UNION ALL
SELECT 3 num UNION ALL
SELECT 4 num UNION ALL
SELECT 5 num UNION ALL
SELECT 6 num UNION ALL
SELECT 7 num UNION ALL
SELECT 8 num UNION ALL
SELECT 9 num
) ones
CROSS JOIN
(
SELECT 0 num UNION ALL
SELECT 10 num UNION ALL
SELECT 20 num UNION ALL
SELECT 30 num UNION ALL
SELECT 40 num UNION ALL
SELECT 50 num UNION ALL
SELECT 60 num UNION ALL
SELECT 70 num UNION ALL
SELECT 80 num UNION ALL
SELECT 90 num
) tens
CROSS JOIN
(
SELECT 0 num UNION ALL
SELECT 100 num UNION ALL
SELECT 200 num UNION ALL
SELECT 300 num
) hundreds
WHERE DATE_ADD('2020-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) < '2021-01-01'
ORDER BY dt
LIMIT 10;
"""



# Query 8: Count rentals per day between 2005-01-01 and 2021-01-01 using a generated calendar
query = """
SELECT days.dt, COUNT(r.rental_id) num_rentals
FROM rental r
RIGHT OUTER JOIN
( SELECT DATE_ADD('2005-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) dt
FROM 
(
SELECT 0 num UNION ALL
SELECT 1 num UNION ALL
SELECT 2 num UNION ALL
SELECT 3 num UNION ALL
SELECT 4 num UNION ALL
SELECT 5 num UNION ALL
SELECT 6 num UNION ALL
SELECT 7 num UNION ALL
SELECT 8 num UNION ALL
SELECT 9 num
) ones
CROSS JOIN
(
SELECT 0 num UNION ALL
SELECT 10 num UNION ALL
SELECT 20 num UNION ALL
SELECT 30 num UNION ALL
SELECT 40 num UNION ALL
SELECT 50 num UNION ALL
SELECT 60 num UNION ALL
SELECT 70 num UNION ALL
SELECT 80 num UNION ALL
SELECT 90 num
) tens
CROSS JOIN
(
SELECT 0 num UNION ALL
SELECT 100 num UNION ALL
SELECT 200 num UNION ALL
SELECT 300 num
) hundreds
WHERE DATE_ADD('2005-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) < '2021-01-01'
) days
ON days.dt = date(r.rental_date)
GROUP BY days.dt
ORDER BY days.dt
LIMIT 10;
"""



# Query 9: Natural join customers with rentals to list customer names and rental dates
query = """
SELECT c.first_name, c.last_name, date(r.rental_date)
FROM customer c
NATURAL JOIN rental r;
"""



# Query 10: Natural join using a subquery to list limited customer rental info
query = """
SELECT cust.first_name, cust.last_name, date(r.rental_date)
FROM 
(
SELECT customer_id, first_name, last_name
FROM customer
) cust
NATURAL JOIN rental r
LIMIT 10;
"""


# Exercise 10-1
# Using the following table definitions and data, write a query that returns each cus‐
# tomer name along with their total payments:
#  Customer:
# Customer_id Name
# ----------- ---------------
# 1 John Smith
# 2 Kathy Jones
# 3 Greg Oliver
#  Payment:
# Payment_id Customer_id Amount
# ---------- ----------- --------
# 101 1 8.99
# 102 3 4.99
# 103 1 7.99
# Include all customers, even if no payment records exist for that customer.


# Query 11: Exercise 10-1 – total payments per customer using left outer join
query = """
SELECT CONCAT(c.first_name,' ', c.last_name) NAME, SUM(p.amount) Amount
FROM customer c
LEFT OUTER JOIN payment p
ON c.customer_id=p.customer_id
GROUP BY c.customer_id
LIMIT 5;
"""



# Exercise 10-2
# Reformulate your query from Exercise 10-1 to use the other outer join type (e.g., if
# you used a left outer join in Exercise 10-1, use a right outer join this time) such that
# the results are identical to Exercise 10-1.


# Query 12: Exercise 10-2 – same result using right outer join
query = """
SELECT CONCAT(c.first_name,' ', c.last_name) NAME, SUM(p.amount) Amount
FROM payment p 
RIGHT OUTER JOIN customer c
ON p.customer_id=c.customer_id
GROUP BY c.customer_id
LIMIT 5;
"""



# Exercise 10-3 (Extra Credit)
# Devise a query that will generate the set {1, 2, 3, ..., 99, 100}. (Hint: use a cross join
# with at least two from clause subqueries.)


# Query 13: Exercise 10-3 – generate numbers 1-100 using cross join of digit tables
query = """
SELECT ones.num + tens.num +1 AS _number
FROM 
(
SELECT 0 num UNION ALL
SELECT 1 num UNION ALL
SELECT 2 num UNION ALL
SELECT 3 num UNION ALL
SELECT 4 num UNION ALL
SELECT 5 num UNION ALL
SELECT 6 num UNION ALL
SELECT 7 num UNION ALL
SELECT 8 num UNION ALL
SELECT 9 num
) ones
CROSS JOIN
(
SELECT 0 num UNION ALL
SELECT 10 num UNION ALL
SELECT 20 num UNION ALL
SELECT 30 num UNION ALL
SELECT 40 num UNION ALL
SELECT 50 num UNION ALL
SELECT 60 num UNION ALL
SELECT 70 num UNION ALL
SELECT 80 num UNION ALL
SELECT 90 num
) tens
ORDER BY _number
LIMIT 10;
"""



# Execute query
results = executor.execute_query(query)


print(results)
executor.close()