from execute_sql import main


executor = main()


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

# Execute query
results = executor.execute_query(query)

print(results)
executor.close()
 