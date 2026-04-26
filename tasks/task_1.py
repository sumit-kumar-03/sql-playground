from execute_sql import main


executor = main()



###############
# learning sql by alan beaulieu - Chapter - 3
###############


# Show all databases
query = "SHOW DATABASES;"


# Show all tables
query = "SHOW TABLES;"


# Ex 3.1 - Retrieve the actor ID, first name, and last name for all actors. 
# Sort by last name and then by first name.
query = "SELECT actor_id, first_name, last_name FROM actor ORDER BY last_name, first_name;"


# Ex 3.2 - Retrieve the actor ID, first name, and last name 
# for all actors whose last name equals 'WILLIAMS' or 'DAVIS'.
query = "SELECT actor_id, first_name, last_name FROM actor WHERE last_name='WILLIAMS' or last_name='DAVIS';"


# Ex 3.3 - Write a query against the rental table that returns 
# the IDs of the customers who ren‐ ted a film on July 5, 2005 
# (use the rental.rental_date column, and you can use the date() function to ignore the time component). 
# Include a single row for each distinct customer ID.
query = "SELECT DISTINCT customer_id FROM rental WHERE date(rental_date)='2005-07-05';"


# Ex 3.4 - Fill in the blanks (denoted by <#>) for this multitable query to achieve the following
# results:
# mysql> SELECT c.email, r.return_date
#  -> FROM customer c
#  -> INNER JOIN rental <1>
#  -> ON c.customer_id = <2>
#  -> WHERE date(r.rental_date) = '2005-06-14'
#  -> ORDER BY <3> <4>;
# +---------------------------------------+---------------------+
# | email | return_date |
# +---------------------------------------+---------------------+
# | DANIEL.CABRAL@sakilacustomer.org | 2005-06-23 22:00:38 |
# | TERRANCE.ROUSH@sakilacustomer.org | 2005-06-23 21:53:46 |
# | MIRIAM.MCKINNEY@sakilacustomer.org | 2005-06-21 17:12:08 |
query = "SELECT c.email, r.return_date FROM customer c INNER JOIN rental r ON c.customer_id = r.customer_id WHERE date(r.rental_date) = '2005-06-14' ORDER BY r.return_date DESC"



###############
# learning sql by alan beaulieu - Chapter - 4
###############



# Equality condition
query = "SELECT DISTINCT c.first_name FROM customer c INNER JOIN rental r ON c.customer_id=r.customer_id WHERE year(r.rental_date)=2005 LIMIT 5;"

# Inequality condition
query = "SELECT DISTINCT c.first_name FROM customer c INNER JOIN rental r ON c.customer_id=r.customer_id WHERE year(r.rental_date)!=2005 LIMIT 5;"
query = "SELECT DISTINCT c.first_name FROM customer c INNER JOIN rental r ON c.customer_id=r.customer_id WHERE year(r.rental_date)<>2005 LIMIT 5;"

# Range
query = "SELECT DISTINCT c.first_name FROM customer c INNER JOIN rental r ON c.customer_id=r.customer_id WHERE year(r.rental_date)>2005 LIMIT 5;"
query = "SELECT DISTINCT c.first_name FROM customer c INNER JOIN rental r ON c.customer_id=r.customer_id WHERE year(r.rental_date)<2005 LIMIT 5;"

# BETWEEN operator
query = "SELECT customer_id, date(rental_date) FROM rental WHERE rental_date BETWEEN '2005-06-14' and '2005-06-16' LIMIT 5;"

# IN operator
query = "SELECT title, rating FROM film WHERE rating IN ('G','PG') LIMIT 5;"

# NOT IN
query = "SELECT title, rating FROM film WHERE rating NOT IN ('G','PG') LIMIT 5;"

# wildcard _ 'exactly one character' , % ' any number of character'
query = "SELECT title, rating FROM film WHERE title LIKE '_A%' LIMIT 5;"

# regex
query = "SELECT first_name FROM customer WHERE first_name REGEXP '^[XYZ]';"


# Exercise 4-1
# Which of the payment IDs would be returned by the following filter conditions?
# customer_id <> 5 AND (amount > 8 OR date(payment_date) = '2005-08-23')
query = "SELECT DISTINCT payment_id FROM payment WHERE customer_id <> 5 AND (amount > 8 OR date(payment_date) = '2005-08-23') AND payment_id BETWEEN 101 AND 120;"


# Exercise 4-2
# Which of the payment IDs would be returned by the following filter conditions?
# customer_id = 5 AND NOT (amount > 6 OR date(payment_date) = '2005-06-19')
query = "SELECT DISTINCT payment_id FROM payment WHERE customer_id = 5 AND NOT (amount > 6 OR date(payment_date) = '2005-06-19') AND payment_id BETWEEN 101 AND 120;"


# Exercise 4-3
# Construct a query that retrieves all rows from the payments table where the amount
# is either 1.98, 7.98, or 9.98.
query = "SELECT * FROM payment WHERE amount IN (1.98, 7.98, 9.98);"


# Exercise 4-4
# Construct a query that finds all customers whose last name contains an A in the sec‐
# ond position and a W anywhere after the A.
query = "SELECT * from customer WHERE last_name LIKE '_A%W%'"



###############
# learning sql by alan beaulieu - Chapter - 5
###############



# JOINS
query = "SELECT c.first_name, a.address FROM customer c INNER JOIN address a ON a.address_id=c.address_id LIMIT 5;"


# Multi Table JOINS
query = "SELECT c.first_name, ct.city FROM customer c INNER JOIN address a ON c.address_id=a.address_id INNER JOIN city ct ON a.city_id=ct.city_id LIMIT 5;"


# Using Subqueries as Tables
query = "SELECT c.first_name, addr.city FROM customer c INNER JOIN (SELECT a.address_id, ct.city FROM address a INNER JOIN city ct ON ct.city_id=a.city_id) addr ON addr.address_id=c.address_id LIMIT 5;"


# Exercise 5-1
# Fill in the blanks (denoted by <#>) for the following query to obtain the results that
# follow:
# mysql> SELECT c.first_name, c.last_name, a.address, ct.city
#  -> FROM customer c
#  -> INNER JOIN address <1>
#  -> ON c.address_id = a.address_id
#  -> INNER JOIN city ct
#  -> ON a.city_id = <2>
#  -> WHERE a.district = 'California';
# +------------+-----------+------------------------+----------------+
# | first_name | last_name | address | city |
# +------------+-----------+------------------------+----------------+
# | PATRICIA | JOHNSON | 1121 Loja Avenue | San Bernardino |
# | BETTY | WHITE | 770 Bydgoszcz Avenue | Citrus Heights |
# | ALICE | STEWART | 1135 Izumisano Parkway | Fontana |
# | ROSA | REYNOLDS | 793 Cam Ranh Avenue | Lancaster |
# | RENEE | LANE | 533 al-Ayn Boulevard | Compton |
# | KRISTIN | JOHNSTON | 226 Brest Manor | Sunnyvale |
# | CASSANDRA | WALTERS | 920 Kumbakonam Loop | Salinas |
# | JACOB | LANCE | 1866 al-Qatif Avenue | El Monte |
# | RENE | MCALISTER | 1895 Zhezqazghan Drive | Garden Grove |
# +------------+-----------+------------------------+----------------+
# 9 rows in set (0.00 sec)
query="""SELECT c.first_name, c.last_name, a.address, ct.city
FROM customer c
INNER JOIN address a
ON c.address_id = a.address_id
INNER JOIN city ct
ON a.city_id = ct.city_id
WHERE a.district = 'California';
"""


# Exercise 5-2
# Write a query that returns the title of every film in which an actor with the first name
# JOHN appeared.
# Test Your Knowledge | 99
query = """SELECT f.title, a.first_name, a.last_name
FROM film f
INNER JOIN film_actor fa
ON fa.film_id = f.film_id
INNER JOIN actor a
ON a.actor_id = fa.actor_id
WHERE a.first_name = "JOHN"
"""


# Exercise 5-3
# Construct a query that returns all addyresses that are in the same city. You will need to
# join the address table to itself, and each row should include two different addresses.
query = """SELECT a.address, nxt_a.address
FROM address a
INNER JOIN address nxt_a
ON a.city_id=nxt_a.city_id
WHERE a.address_id!=nxt_a.address_id;
"""



###############
# learning sql by alan beaulieu - Chapter - 6
###############



# Set Operators- union all (Duplicates will present)
query = """SELECT '1st' typ, c.first_name, c.last_name
FROM customer c
UNION ALL
SELECT '2nd' typ, a.first_name, a.last_name
FROM actor a
LIMIT 10;"""


query = """SELECT c.first_name, c.last_name
FROM customer c
WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
UNION ALL
SELECT a.first_name, a.last_name
FROM actor a
WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%'
LIMIT 10;
"""


# Set Operators - union (NO duplicates)
query = """SELECT c.first_name, c.last_name
FROM customer c
WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
UNION
SELECT a.first_name, a.last_name
FROM actor a
WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%'
LIMIT 10;
"""


# Set Operators - Intersect (Common in both)
query = """SELECT c.first_name, c.last_name
FROM customer c
WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
INTERSECT
SELECT a.first_name, a.last_name
FROM actor a
WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%'
LIMIT 10;
"""


# Set Operators - except (first minus second)
query = """SELECT a.first_name, a.last_name
FROM actor a
WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%'
EXCEPT
SELECT c.first_name, c.last_name
FROM customer c
WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
LIMIT 10;
"""


# Exercise 6-1
# If set A = {L M N O P} and set B = {P Q R S T}, what sets are generated by the follow‐
# ing operations?
# • A union B - {L M N O P Q R S T}
# • A union all B - {L M N O P P Q R S T}
# • A intersect B - {P}
# • A except B - {L M N O}


# Exercise 6-2
# Write a compound query that finds the first and last names of all actors and custom‐
# ers whose last name starts with L.
query = """SELECT a.first_name, a.last_name
FROM actor a
WHERE a.last_name LIKE 'L%'
UNION ALL
SELECT c.first_name, c.last_name
FROM customer c
WHERE c.last_name LIKE 'L%'
LIMIT 10;
"""

# Exercise 6-3
# Sort the results from Exercise 6-2 by the last_name column.
query = """SELECT a.first_name, a.last_name
FROM actor a
WHERE a.last_name LIKE 'L%'
UNION ALL
SELECT c.first_name, c.last_name
FROM customer c
WHERE c.last_name LIKE 'L%'
ORDER BY last_name
LIMIT 10;
"""


# Execute query
results = executor.execute_query(query)

print(results)
executor.close()
 