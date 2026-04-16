from execute_sql import main


executor = main()


###############
# Chapter - 8
###############


## SQL ORDER OF EXECUTION
# SELECT
# FROM
# WHERE
# GROUP BY
# HAVING
# ORDER BY
# LIMIT



# Query 1: Basic select to get 5 customer IDs
query = """
SELECT customer_id 
FROM rental
LIMIT 5;
"""


# Query 2: Group by customer_id to count rentals per customer
query = """
SELECT customer_id  AS cust, COUNT(customer_id) AS cnt
FROM rental
GROUP BY customer_id
LIMIT 5;
"""


# Query 3: Group by customer_id and order by the count in descending order
query = """
SELECT customer_id  AS cust, COUNT(customer_id) AS cnt
FROM rental
GROUP BY customer_id
ORDER BY cnt DESC
LIMIT 5;
"""


# Query 4: Group by customer_id, filter groups having count >= 40, and order descending
query = """
SELECT customer_id  AS cust, COUNT(customer_id) AS cnt
FROM rental
GROUP BY customer_id
HAVING cnt >= 40
ORDER BY cnt DESC;
"""




# Query 5: Calculate global aggregate statistics (max, min, avg, sum) from customer rental counts subquery
query = """
SELECT 
    MAX(cnt) AS _max,
    MIN(cnt) AS _min,
    AVG(cnt) AS _avg,
    SUM(cnt) AS _sum
FROM (
    SELECT customer_id, COUNT(*) AS cnt
    FROM rental
    GROUP BY customer_id
) AS customer_counts;
"""



# Query 6: Get aggregate payment statistics (max, min, avg, sum) per customer, top 5 by sum
query = """
SELECT customer_id AS cust,
    MAX(amount) AS _max,
    MIN(amount) AS _min,
    AVG(amount) AS _avg,
    SUM(amount) AS _sum
FROM payment
GROUP BY customer_id
ORDER BY _sum DESC
LIMIT 5;
"""



# Query 7: Count total payments and distinct customers making payments
query = """
SELECT COUNT(customer_id) AS num_pay,
COUNT(DISTINCT customer_id) AS num_cust
FROM payment;
"""


# Query 8: Find the maximum rental duration in days across all rentals
query = """
SELECT MAX(datediff(return_date, rental_date))
FROM rental;
"""


# Query 9: Find the maximum rental duration in days per customer, top 5 descending
query = """
SELECT customer_id AS cust, 
MAX(datediff(return_date, rental_date)) AS _max
FROM rental
GROUP BY customer_id
ORDER by _max DESC
LIMIT 5;
"""



# Query 10: Count occurrences of actor and film rating combinations
query = """
SELECT fa.actor_id AS fa_a, f.rating AS f_r, count(*)
FROM film_actor AS fa
INNER JOIN film AS f
ON fa.film_id = f.film_id
GROUP BY fa_a, f_r
ORDER BY fa_a, f_r 
LIMIT 12;
"""



# Query 11: Count the number of rentals per year
query = """
SELECT EXTRACT(YEAR FROM rental_date) AS _year, COUNT(rental_date)
FROM rental
GROUP BY _year
ORDER BY _year DESC;
"""



# Query 12: Count occurrences of actor and film rating combinations with ROLLUP for subtotals
query = """
SELECT fa.actor_id AS fa_a, f.rating AS f_r, count(*)
FROM film_actor AS fa
INNER JOIN film AS f
ON fa.film_id = f.film_id
GROUP BY fa_a, f_r WITH ROLLUP
ORDER BY fa_a, f_r 
LIMIT 12;
"""



# Query 13: Count occurrences of actor and film rating combinations, filtering for 'G'/'PG' ratings and count > 9
query = """
SELECT fa.actor_id AS fa_a, f.rating AS f_r, count(*) AS _count
FROM film_actor AS fa
INNER JOIN film AS f
ON fa.film_id = f.film_id
WHERE f.rating IN ('G','PG')
GROUP BY fa_a, f_r
HAVING _count >9
ORDER BY fa_a, f_r 
LIMIT 12;
"""


# Ex 8.1 Construct a query that counts the number of rows in the payment table
query = """
SELECT COUNT(*)
FROM payment;
"""


# Ex 8.2 Modify your query from Exercise 8-1 to count the number of payments made by each
# customer. Show the customer ID and the total amount paid for each customer.
query = """
SELECT customer_id AS cust, count(*) num_payment, SUM(amount) AS total_amt
FROM payment
GROUP BY customer_id
LIMIT 5;
"""


# Ex 8.3 Modify your query from Exercise 8-2 to include only those customers who have
# made at least 40 payments.
query = """
SELECT customer_id AS cust, count(*) num_payment, SUM(amount) AS total_amt
FROM payment
GROUP BY customer_id
HAVING num_payment >= 40
LIMIT 5;
"""




###############
# Chapter - 9
###############



# Query 14: Subquery using IN to find cities located in India
query = """
SELECT city_id, city
FROM city 
WHERE country_id IN
(SELECT country_id 
FROM country 
WHERE country = 'India')
LIMIT 10;
"""



# Query 15: Subquery using <> to find cities NOT located in India
query = """
SELECT city_id, city
FROM city 
WHERE country_id <>
(SELECT country_id 
FROM country 
WHERE country = 'India')
LIMIT 10;
"""



# Query 16: Subquery using IN with <> to find cities in countries other than India
query = """
SELECT city_id, city
FROM city 
WHERE country_id IN
(SELECT country_id 
FROM country 
WHERE country <> 'India')
LIMIT 10;
"""



# Query 17: Subquery using NOT IN with <> (effectively finds cities in India)
query = """
SELECT city_id, city
FROM city 
WHERE country_id NOT IN
(SELECT country_id 
FROM country 
WHERE country <> 'India')
LIMIT 10;
"""


# Execute query
results = executor.execute_query(query)


print(results)
executor.close()