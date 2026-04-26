from execute_sql import main


executor = main()


###############
# learning sql by alan beaulieu - Chapter - 8
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
# learning sql by alan beaulieu - Chapter - 9
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



# Query 18: Subquery with IN to find cities in Nepal or Bhutan
query = """
SELECT city_id, city
FROM city 
WHERE country_id IN
(SELECT country_id
FROM country
WHERE country = 'Nepal' OR country = 'Bhutan');
"""



# Query 19: Subquery with IN using an IN list to find cities in Nepal or Sri Lanka
query = """
SELECT city_id, city
FROM city 
WHERE country_id IN
(SELECT country_id
FROM country
WHERE country IN ('Nepal','Sri Lanka'));
"""



# Query 20: Subquery using <> ALL to find cities that are ONLY in Nepal or Sri Lanka
query = """
SELECT city
FROM city
WHERE country_id <> ALL 
(SELECT country_id 
FROM country 
WHERE country NOT IN ('Nepal','Sri Lanka'));
"""



# Query 21: Subquery using <> ALL to find customers who never made a payment of 0
query = """
SELECT first_name
FROM customer 
WHERE customer_id <> ALL
( SELECT customer_id 
FROM payment
WHERE amount = 0)
LIMIT 10;
"""



# Query 22: Subquery using > ALL to find customers who rented more films than anyone in North America
query = """
SELECT customer_id , count(*)
FROM rental
GROUP BY customer_id
HAVING count(*) > ALL
(
SELECT count(*)
FROM rental r
INNER JOIN customer c
ON r.customer_id = c.customer_id
INNER JOIN address a
ON c.address_id = a.address_id
INNER JOIN city ct
ON a.city_id = ct.city_id
INNER JOIN country co
ON ct.country_id = co.country_id
WHERE co.country IN ('Canada', 'Mexico', 'United States')
GROUP BY r.customer_id
);
"""



# Query 23: Subquery using > ANY to find customers whose total payments exceed the total payments of at least one South American country
query = """
SELECT customer_id,  SUM(amount)
FROM payment
GROUP BY customer_id 
HAVING SUM(amount) > ANY
(
SELECT SUM(p.amount)
FROM payment p
INNER JOIN customer c
ON p.customer_id = c.customer_id
INNER JOIN address a
ON c.address_id = a.address_id
INNER JOIN city ct
ON a.city_id = ct.city_id
INNER JOIN country co
ON ct.country_id = co.country_id
WHERE co.country IN ('Bolivia','Paraguay','Chile')
GROUP BY co.country  
);Exercise 9-1
# Construct a query against the film table that uses a filter condition with a noncorre‐
# lated subquery against the category table to find all action films (category.name =
# 'Action').
# Exercise 9-2
# Rework the query from Exercise 9-1 using a correlated subquery against the category
# and film_category tables to achieve the same results.
# Exercise 9-3
# Join the following query to a subquery against the film_actor table to show the level
# of each actor:
# SELECT 'Hollywood Star' level, 30 min_roles, 99999 max_roles
# UNION ALL
# SELECT 'Prolific Actor' level, 20 min_roles, 29 max_roles
# UNION ALL
# SELECT 'Newcomer' level, 1 min_roles, 19 max_roles

"""



# Query 24: Multiple independent subqueries to find actors with last name MONROE in PG rated films
query = """
SELECT fa.actor_id, fa.film_id
FROM film_actor fa
WHERE fa.actor_id IN
(SELECT actor_id 
FROM actor 
WHERE last_name = 'MONROE')
AND
fa.film_id IN
(SELECT film_id FROM film WHERE rating = 'PG');
"""



# Query 25: Multi-column subquery using IN to find actors with last name MONROE in PG rated films
query = """
SELECT actor_id, film_id
FROM film_actor
WHERE (actor_id, film_id ) IN
(SELECT a.actor_id, f.film_id
FROM actor a
CROSS JOIN film f
WHERE a.last_name = 'MONROE'
AND f.rating = 'PG');
"""



# Query 26: Correlated subquery to find customers who have rented exactly 20 times
query = """
SELECT c.first_name, c.last_name
FROM customer c
WHERE 20 =
(SELECT count(*)
FROM rental r 
WHERE r.customer_id = c.customer_id);
"""



# Query 27: Correlated subquery with EXISTS to find customers who rented before 2005-05-25
query = """
SELECT c.first_name, c.last_name
FROM customer c
WHERE EXISTS
( SELECT 1 
FROM rental r
WHERE r.customer_id = c.customer_id
AND date(r.rental_date) < '2005-05-25');
"""



# Query 28: Correlated subquery with NOT EXISTS to find actors who have never been in an 'R' rated film
query = """
SELECT a.first_name, a.last_name
FROM actor a
WHERE NOT EXISTS
( SELECT 1
FROM film_actor fa
INNER JOIN film f
ON fa.film_id = f.film_id
WHERE fa.actor_id = a.actor_id
AND f.rating = 'R');
)
"""



# Query 29: Correlated scalar subquery used in an UPDATE statement
query = """
UPDATE customer c
SET c.last_update = 
(SELECT max(r.rental_date) 
FROM rental r
WHERE r.customer_id = c.customer_id);
"""



# Query 30: Correlated scalar subquery in an UPDATE statement, protected by an EXISTS correlated subquery
query = """
UPDATE customer c
SET c.last_update = 
(SELECT max(r.rental_date) 
FROM rental r
WHERE r.customer_id = c.customer_id)
WHERE EXISTS
(SELECT 1 
FROM rental r
WHERE r.customer_id = c.customer_id);
"""



# Query 31: Inline view (subquery in FROM clause) to aggregate payments before joining with customer
query = """
SELECT c.first_name, c.last_name, pymnt.num_rentals, pymnt.tot_payments
FROM customer c
INNER JOIN
(SELECT customer_id, COUNT(*) AS num_rentals, SUM(amount) AS tot_payments
FROM payment
GROUP BY customer_id ) pymnt
ON c.customer_id = pymnt.customer_id
LIMIT 10;
"""



# Query 32: Building a derived table using UNION ALL
query = """
SELECT 'Small Fry' name, 0 low_limit, 74.99 high_limit
UNION ALL
SELECT 'Average Joes' name, 75 low_limit, 149.99 high_limit
UNION ALL
SELECT 'Heavy Hitters' name, 150 low_limit, 9999999.99 high_limit;
"""


# Query 33: Joining two inline views (one aggregating payments, one derived table from UNION ALL)
query = """
SELECT pymnt_grps.name, count(*) num_customers
FROM
( SELECT customer_id, count(*) num_rentals, sum(amount) tot_payments
FROM payment
GROUP BY customer_id 
) pymnt
INNER JOIN
(SELECT 'Small Fry' name, 0 low_limit, 74.99 high_limit
UNION ALL
SELECT 'Average Joes' name, 75 low_limit, 149.99 high_limit
UNION ALL
SELECT 'Heavy Hitters' name, 150 low_limit, 9999999.99 high_limit
) pymnt_grps
ON pymnt.tot_payments BETWEEN 
pymnt_grps.low_limit AND pymnt_grps.high_limit
GROUP BY pymnt_grps.name;
"""



# Query 34: Standard join and aggregation without inline views
query = """
SELECT c.first_name, c.last_name, ct.city, sum(p.amount) tot_payments, count(*) tot_rentals
FROM payment p
INNER JOIN customer c
ON p.customer_id = c.customer_id
INNER JOIN address a
ON c.address_id = a.address_id
INNER JOIN city ct
ON a.city_id = ct.city_id
GROUP BY p.customer_id
ORDER BY tot_payments DESC
LIMIT 5;
"""



# Query 35: Same logic as previous query but using an inline view for aggregation to improve performance
query = """
SELECT c.first_name, c.last_name, ct.city, pymnt.tot_payments, pymnt.tot_rentals
FROM (
SELECT customer_id, sum(amount) tot_payments, count(*) tot_rentals
FROM payment
GROUP BY customer_id
) pymnt
INNER JOIN customer c
ON pymnt.customer_id = c.customer_id
INNER JOIN address a
ON c.address_id = a.address_id
INNER JOIN city ct
ON a.city_id = ct.city_id
ORDER BY pymnt.tot_payments DESC
LIMIT 5;
"""



# Query 36: Common Table Expressions (CTEs) using the WITH clause to break down a complex query
query = """
WITH actors_s AS
(SELECT actor_id, first_name, last_name
FROM actor
WHERE last_name LIKE 'S%'
),
actors_s_pg AS
( SELECT s.actor_id, s.first_name, s.last_name, f.film_id, f.title
FROM actors_s s
INNER JOIN film_actor fa
ON s.actor_id = fa.actor_id
INNER JOIN film f
ON f.film_id = fa.film_id
WHERE f.rating = 'PG'
),
actors_s_pg_revenue AS
( SELECT spg.first_name, spg.last_name, p.amount
FROM actors_s_pg spg
INNER JOIN inventory i
ON i.film_id = spg.film_id
INNER JOIN rental r
ON i.inventory_id = r.inventory_id
INNER JOIN payment p
ON r.rental_id = p.rental_id
) 
SELECT spg_rev.first_name, spg_rev.last_name, sum(spg_rev.amount) tot_revenue
FROM actors_s_pg_revenue  spg_rev
GROUP BY spg_rev.first_name, spg_rev.last_name
ORDER BY 3 DESC;
"""



# Exercise 9-1
# Construct a query against the film table that uses a filter condition with a noncorre‐
# lated subquery against the category table to find all action films (category.name =
# 'Action').

query = """
SELECT title
FROM film
WHERE film_id IN
(SELECT film_id 
FROM film_category fc
INNER JOIN category c
ON fc.category_id = c.category_id
WHERE c.name='Action')
LIMIT 5;
"""



# Exercise 9-2
# Rework the query from Exercise 9-1 using a correlated subquery against the category
# and film_category tables to achieve the same results.

query = """
SELECT title
FROM film f
WHERE EXISTS
( SELECT 1
FROM film_category fc
INNER JOIN category c
ON fc.category_id = c.category_id
WHERE fc.film_id = f.film_id
AND c.name = 'Action')
LIMIT 5;
"""



# Exercise 9-3
# Join the following query to a subquery against the film_actor table to show the level
# of each actor:
# SELECT 'Hollywood Star' level, 30 min_roles, 99999 max_roles
# UNION ALL
# SELECT 'Prolific Actor' level, 20 min_roles, 29 max_roles
# UNION ALL
# SELECT 'Newcomer' level, 1 min_roles, 19 max_roles


query = """
SELECT actor_info.first_name, actor_info.last_name, star_level.level
FROM (
SELECT a.first_name, a.last_name, count(*) num_roles
FROM actor a
INNER JOIN film_actor fa
ON a.actor_id = fa.actor_id
GROUP BY a.actor_id
) actor_info
INNER JOIN (
SELECT 'Hollywood Star' level, 30 min_roles, 99999 max_roles
UNION ALL
SELECT 'Prolific Actor' level, 20 min_roles, 29 max_roles
UNION ALL
SELECT 'Newcomer' level, 1 min_roles, 19 max_roles
) star_level
ON actor_info.num_roles 
BETWEEN star_level.min_roles AND star_level.max_roles
LIMIT 5;
"""


# Execute query
results = executor.execute_query(query)


print(results)
executor.close()