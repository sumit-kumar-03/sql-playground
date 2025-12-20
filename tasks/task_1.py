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


# Execute query
results = executor.execute_query(query)

print(results)
executor.close()
 