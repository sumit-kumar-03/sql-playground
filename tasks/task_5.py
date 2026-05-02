from execute_sql import main


executor = main()


###############
# learning sql by alan beaulieu - Chapter - 11
###############



# Query 1: Simple CASE to label customers as ACTIVE or INACTIVE
query = """
SELECT first_name, last_name, 
CASE
WHEN active = 1 THEN 'ACTIVE'
ELSE 'INACTIVE'
END activity_type
FROM customer
LIMIT 10;
"""



# Example of a searched CASE expression
## SEARCHED CASE
"""
CASE 
WHEN expression_1 THEN value_1
WHEN expression_2 THEN value_2
WHEN expression_3 THEN value_3
ELSE default_value
END
"""



# Query 2: Searched CASE to count rentals per customer when active = 0
query = """
SELECT c.first_name, c.last_name,
CASE
WHEN active = 0 THEN 0
ELSE (SELECT count(*) 
FROM rental r 
WHERE r.customer_id = c.customer_id)
END num_rental
FROM customer c
ORDER BY num_rental
LIMIT 10;
"""



# Example of a simple CASE expression
## SIMPLE CASE
"""
CASE value_to_compare_with
WHEN value_to_be_compared_1 THEN value_1
WHEN value_to_be_compared_2 THEN value_2
WHEN value_to_be_compiled_3 THEN value_3
ELSE default_value
END
"""



# Query 3: Aggregate rentals per month (May, June, July) using CASE expressions
query = """
SELECT 
SUM(CASE 
WHEN monthname(rental_date)='May' 
THEN 1 ELSE 0 END
) May_rentals,
SUM(CASE 
WHEN monthname(rental_date)='June' 
THEN 1 ELSE 0 END
) June_rentals,
SUM(CASE 
WHEN monthname(rental_date)='July' 
THEN 1 ELSE 0 END
) July_rentals
FROM rental
WHERE rental_date BETWEEN '2005-05-01' AND '2005-08-01'; 
"""



# Query 4: Determine if actors have appeared in films with ratings G, PG, and NC-17 using EXISTS
query = """
SELECT a.first_name, a.last_name,
CASE
WHEN EXISTS (
SELECT 1 FROM film_actor fa 
INNER JOIN film f
ON fa.film_id=f.film_id
WHERE fa.actor_id = a.actor_id AND f.rating = 'G')
THEN 'Y'
ELSE 'N'
END g_actor,
CASE
WHEN EXISTS (
SELECT 1 FROM film_actor fa 
INNER JOIN film f
ON fa.film_id=f.film_id
WHERE fa.actor_id = a.actor_id AND f.rating = 'PG')
THEN 'Y'
ELSE 'N'
END pg_actor,
CASE
WHEN EXISTS (
SELECT 1 FROM film_actor fa 
INNER JOIN film f
ON fa.film_id=f.film_id
WHERE fa.actor_id = a.actor_id AND f.rating = 'NC-17')
THEN 'Y'
ELSE 'N'
END nc17_actor
FROM actor a
LIMIT 10;
"""



# Query 5: Same actor rating checks filtered to actors with names starting with 'S'
query = """
SELECT a.first_name, a.last_name,
CASE
WHEN EXISTS (
SELECT 1 FROM film_actor fa 
INNER JOIN film f
ON fa.film_id=f.film_id
WHERE fa.actor_id = a.actor_id AND f.rating = 'G')
THEN 'Y'
ELSE 'N'
END g_actor,
CASE
WHEN EXISTS (
SELECT 1 FROM film_actor fa 
INNER JOIN film f
ON fa.film_id=f.film_id
WHERE fa.actor_id = a.actor_id AND f.rating = 'PG')
THEN 'Y'
ELSE 'N'
END pg_actor,
CASE
WHEN EXISTS (
SELECT 1 FROM film_actor fa 
INNER JOIN film f
ON fa.film_id=f.film_id
WHERE fa.actor_id = a.actor_id AND f.rating = 'NC-17')
THEN 'Y'
ELSE 'N'
END nc17_actor
FROM actor a
WHERE a.last_name LIKE 'S%' OR a.first_name LIKE 'S%'
LIMIT 10;
"""




# Query 6: Use CASE on subquery count to indicate film availability status
query = """
SELECT f.title, 
CASE (SELECT count(*) 
FROM inventory i 
WHERE f.film_id = i.film_id )
WHEN 0 THEN 'OUT OF STOCK'
WHEN 1 THEN 'Scarce'
WHEN 2 THEN 'Scarce'
WHEN 3 THEN 'Available'
WHEN 4 THEN 'Available'
ELSE 'Common'
END film_availability
FROM film f
LIMIT 10;
"""



# Query 7: Compute total, count, and average payment amounts per customer
query = """
SELECT c.first_name, c.last_name,
sum(p.amount) tot_payments_amt,
count(p.amount) num_payments,
sum(p.amount) /
CASE WHEN count(p.amount) = 0 THEN 1
ELSE count(p.amount)
END avg_payment
FROM customer c
LEFT OUTER JOIN payment p
ON c.customer_id = p.customer_id
GROUP BY c.first_name, c.last_name
LIMIT 10;
"""


# Query 8: Use CASE to replace NULL address, city, or country with 'Unknown'
query = """
SELECT c.first_name, c.last_name,
 CASE
 WHEN a.address IS NULL THEN 'Unknown'
 ELSE a.address
 END address,
 CASE
 WHEN ct.city IS NULL THEN 'Unknown'
 ELSE ct.city
 END city,
 CASE
 WHEN cn.country IS NULL THEN 'Unknown'
 ELSE cn.country
 END country
FROM customer c
 LEFT OUTER JOIN address a
 ON c.address_id = a.address_id
 LEFT OUTER JOIN city ct
 ON a.city_id = ct.city_id
 LEFT OUTER JOIN country cn
 ON ct.country_id = cn.country_id
 LIMIT 10;
"""




# Exercise 11-1
# Rewrite the following query, which uses a simple case expression, so that the same
# results are achieved using a searched case expression. Try to use as few when clauses
# as possible.
# SELECT name,
#  CASE name
#  WHEN 'English' THEN 'latin1'
#  WHEN 'Italian' THEN 'latin1'
#  WHEN 'French' THEN 'latin1'
#  WHEN 'German' THEN 'latin1'
#  WHEN 'Japanese' THEN 'utf8'
#  WHEN 'Mandarin' THEN 'utf8'
#  ELSE 'Unknown'
#  END character_set
# FROM language;



# Query 9: Rewrite language charset mapping using a searched CASE expression
query = """
SELECT name,
 CASE 
 WHEN name IN ('English', 'Italian', 'French', 'German') THEN 'latin1'
 WHEN name IN ('Japanese', 'Mandarin' ) THEN 'utf8'
 ELSE 'Unknown'
 END character_set
FROM language
LIMIT 10;
"""


# Exercise 11-2
# Rewrite the following query so that the result set contains a single row with five col‐
# umns (one for each rating). Name the five columns G, PG, PG_13, R, and NC_17.
# mysql> SELECT rating, count(*)
#  -> FROM film
#  -> GROUP BY rating;
# +--------+----------+
# | rating | count(*) |
# +--------+----------+
# | PG | 194 |
# | G | 178 |
# | NC-17 | 210 |
# | PG-13 | 223 |
# | R | 195 |
# +--------+----------+
# 5 rows in set (0.00 sec)




# Query 10: Pivot film rating counts into separate columns using SUM(CASE)
query = """
SELECT 
SUM( CASE
WHEN rating='PG' THEN 1
ELSE 0
END) PG,
SUM( CASE
WHEN rating='G' THEN 1
ELSE 0
END) G,
SUM( CASE
WHEN rating='PG-13' THEN 1
ELSE 0
END) PG_13,
SUM( CASE
WHEN rating='R' THEN 1
ELSE 0
END) R,
SUM( CASE
WHEN rating='NC-17' THEN 1
ELSE 0
END) NC_17
FROM film;
"""



# Execute query
results = executor.execute_query(query)


print(results)
executor.close()