from execute_sql import main


executor = main()


###############
# learning sql by alan beaulieu - Chapter - 12
###############






# Exercise 12-1
# Generate a unit of work to transfer $50 from account 123 to account 789. You will
# need to insert two rows into the transaction table and update two rows in the
# account table. Use the following table definitions/data:
#  Account:
# account_id avail_balance last_activity_date
# ---------- ------------- ------------------
# 123 500 2019-07-10 20:53:27
# 789 75 2019-06-22 15:18:35
#  Transaction:
# txn_id txn_date account_id txn_type_cd amount
# --------- ------------ ----------- ----------- --------
# 1001 2019-05-15 123 C 500
# 1002 2019-06-01 789 C 75
# Use txn_type_cd = 'C' to indicate a credit (addition), and use txn_type_cd = 'D'
# to indicate a debit (subtraction).



# Query 1: Transaction script to transfer $50 from account 123 to account 789 using debit/credit updates and transaction records
"""
START TRANSACTION;

--  Debit from account 123
UPDATE account
SET avail_balance = avail_balance - 50,
    last_activity_date = NOW()
WHERE account_id = 123
  AND avail_balance >= 50;

-- Optional safety check
-- (in real apps you'd check affected rows)

--  Record debit transaction
INSERT INTO transaction (txn_date, account_id, txn_type_cd, amount)
VALUES (NOW(), 123, 'D', 50);

--  Credit to account 789
UPDATE account
SET avail_balance = avail_balance + 50,
    last_activity_date = NOW()
WHERE account_id = 789;

--  Record credit transaction
INSERT INTO transaction (txn_date, account_id, txn_type_cd, amount)
VALUES (NOW(), 789, 'C', 50);

COMMIT;
"""




###############
# learning sql by alan beaulieu - Chapter - 13
###############



# Query 2: Select customers whose last name starts with 'Y'
query = """
SELECT first_name, last_name
FROM customer
WHERE last_name LIKE 'Y%';
"""



# Query 3: Add a simple index on customer.email
query = """
ALTER TABLE customer
ADD INDEX idx_email (email);
"""



# Query 4: Create index on customer.email using CREATE INDEX syntax
query = """
CREATE INDEX idx_email
ON customer (email);
"""



# Query 5: Show indexes defined on the customer table
query = """
SHOW INDEX FROM customer ;
"""



# Query 6: Drop the previously created index on customer.email
query = """
ALTER TABLE customer
DROP INDEX idx_email;
"""



# Query 7: Add a unique index on customer.email to enforce uniqueness
query = """
ALTER TABLE customer
ADD UNIQUE INDEX idx_email (email);
"""



# Query 8: Add composite index on last_name and first_name for faster lookups
query = """
ALTER TABLE customer
ADD INDEX idx_full_name (last_name, first_name);
"""



# Query 9: Explain execution plan for selecting customers with first name starting 'S' and last name starting 'P'
query = """
EXPLAIN
SELECT customer_id, first_name, last_name
FROM customer
WHERE first_name LIKE 'S%' AND last_name LIKE 'P%';
"""



# Query 10: Add foreign key constraint linking customer.address_id to address.address_id
query = """
ALTER TABLE customer
ADD CONSTRAINT fk_customer_address FOREIGN KEY (address_id)
REFERENCES address (address_id) ON DELETE RESTRICT ON UPDATE CASCADE;
"""



# Query 11: Add foreign key constraint linking customer.store_id to store.store_id
query = """
ALTER TABLE customer
ADD CONSTRAINT fk_customer_store FOREIGN KEY (store_id)
REFERENCES store (store_id) ON DELETE RESTRICT ON UPDATE CASCADE;
"""




# Exercise 13-1
# Generate an alter table statement for the rental table so that an error will be
# raised if a row having a value found in the rental.customer_id column is deleted
# from the customer table.

# Query 12: Add foreign key to rental.customer_id referencing customer.customer_id with RESTRICT on delete
query = """
ALTER TABLE rental
ADD CONSTRAINT fk_rental_customer FOREIGN KEY (customer_id)
REFERENCES customer (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE;
"""



# Exercise 13-2
# Generate a multicolumn index on the payment table that could be used by both of the
# following queries:
# SELECT customer_id, payment_date, amount
# FROM payment
# WHERE payment_date > cast('2019-12-31 23:59:59' as datetime);
# SELECT customer_id, payment_date, amount
# FROM payment
# WHERE payment_date > cast('2019-12-31 23:59:59' as datetime)
#  AND am

# Query 13: Add multi-column index on payment.payment_date and amount for query optimization
query = """
ALTER TABLE payment
ADD INDEX idx_pay_d_amt (payment_date, amount);
"""





###############
# learning sql by alan beaulieu - Chapter - 14
###############



# Query 14: Create view customer_vw showing active customers with masked email
query = """
CREATE VIEW customer_vw
(
customer_id,
first_name,
last_name,
email
)
AS 
SELECT
customer_id,
first_name,
last_name,
concat(substr(email,1,2), '*****',substr(email,-4)) email
FROM customer
WHERE active = 1;
"""



# Query 15: Select first_name and masked email from customer_vw
query = """
SELECT first_name, email
FROM customer_vw
LIMIT 10;
"""



# Query 16: Describe the customer_vw view
query = """
describe customer_vw;
"""



# Query 17: Aggregate customers in customer_vw by first name starting with 'J'
query = """
SELECT first_name, count(*), min(last_name), max(last_name)
FROM customer_vw
WHERE first_name LIKE 'J%'
GROUP BY first_name
HAVING count(*) > 1
ORDER BY 1;
"""



# Query 18: Join customer_vw with payments where amount >= 11
query = """
SELECT cv.first_name, cv.last_name, p.amount
FROM customer_vw cv
INNER JOIN payment p
ON cv.customer_id = p.customer_id
WHERE p.amount >= 11;
"""



# Query 19: Create view sales_by_film_category aggregating total sales per category
query = """
CREATE VIEW sales_by_film_category
AS 
SELECT 
 c.name AS category,
 SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r ON p.rental_id = r.rental_id
INNER JOIN inventory AS i ON r.inventory_id = i.inventory_id
INNER JOIN film AS f ON  i.film_id = f.film_id
INNER JOIN film_category AS fc ON f.film_id = fc.film_id
INNER JOIN category AS c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY total_sales DESC; 
"""



# Query 20: Select top 10 categories by sales from sales_by_film_category
query = """
SELECT *
FROM sales_by_film_category
LIMIT 10;
"""



# Query 21: Create view film_stats with film details and related aggregates
query = """
CREATE VIEW film_stats
AS
SELECT f.film_id, f.title, f.description, f.rating,
 (SELECT c.name
 FROM category c
 INNER JOIN film_category fc
 ON c.category_id = fc.category_id
 WHERE fc.film_id = f.film_id) category_name,
 (SELECT count(*)
 FROM film_actor fa
 WHERE fa.film_id = f.film_id
 ) num_actors,
 (SELECT count(*)
 FROM inventory i
 WHERE i.film_id = f.film_id
 ) inventory_cnt,
 (SELECT count(*)
 FROM inventory i
 INNER JOIN rental r
 ON i.inventory_id = r.inventory_id
 WHERE i.film_id = f.film_id
 ) num_rentals
FROM film f;
"""



# Query 22: Select top 10 rows from film_stats view
query = """
SELECT *
FROM film_stats
LIMIT 10
"""



# Query 23: Create view payment_all combining historic and current payments
query = """
CREATE VIEW payment_all
 (payment_id,
 customer_id,
 staff_id,
 rental_id,
 amount,
 payment_date,
 last_update
 )
AS
SELECT payment_id, customer_id, staff_id, rental_id,
 amount, payment_date, last_update
FROM payment_historic
UNION ALL
SELECT payment_id, customer_id, staff_id, rental_id,
 amount, payment_date, last_update
FROM payment_current;
"""



# Query 24: Create view customer_details with detailed customer information
query = """
CREATE VIEW customer_details
AS
SELECT c.customer_id,
 c.store_id,
 c.first_name,
 c.last_name,
 c.address_id,
 c.active,
 c.create_date,
 a.address,
 ct.city,
 cn.country,
 a.postal_code
FROM customer c
 INNER JOIN address a
 ON c.address_id = a.address_id
 INNER JOIN city ct
 ON a.city_id = ct.city_id
 INNER JOIN country cn
 ON ct.country_id = cn.country_id;
"""



# Query 25: Update last_name and active flag for customer_id 1 in customer_details
query = """
UPDATE customer_details
SET last_name = 'SMITH-ALLEN', active = 0
WHERE customer_id = 1;
"""



# Query 26: Update address for customer_id 1 in customer_details
query = """
UPDATE customer_details
SET address = '999 Mockingbird Lane'
WHERE customer_id = 1;
"""


# Query 27: Retrieve all columns for customer_id 1 from customer_details
query = """
SELECT * 
FROM customer_details
WHERE customer_id = 1;
"""



# Query 28: Update last_name, active, and address for customer_id 1 in customer_details
query = """
UPDATE customer_details
SET 
last_name = 'SMITH-ALLEN', 
active = 0,
address = '999 Mockingbird Lane'
WHERE customer_id = 1;
"""



# Query 29: Insert a new customer into customer_details (basic fields)
query = """
INSERT INTO customer_details
(
customer_id, store_id, first_name, last_name,
address_id, active, create_date 
)
VALUES 
(
9998, 1, 'BRIAN', 'SALAZAR', 5, 1, now()
);
"""



# Query 30: Insert a new customer into customer_details including address
query = """
INSERT INTO customer_details
(
customer_id, store_id, first_name, last_name,
address_id, active, create_date, 
address 
)
VALUES 
(
9998, 1, 'BRIAN', 'SALAZAR', 5, 1, now(),
'999 Mockingbird Lane'
);
"""




# Exercise 14-1
# Create a view definition that can be used by the following query to generate the given
# results:
# SELECT title, category_name, first_name, last_name
# FROM film_ctgry_actor
# WHERE last_name = 'FAWCETT';
# +---------------------+---------------+------------+-----------+
# | title | category_name | first_name | last_name |
# +---------------------+---------------+------------+-----------+
# | ACE GOLDFINGER | Horror | BOB | FAWCETT |
# | ADAPTATION HOLES | Documentary | BOB | FAWCETT |
# | CHINATOWN GLADIATOR | New | BOB | FAWCETT |
# | CIRCUS YOUTH | Children | BOB | FAWCETT |
# | CONTROL ANTHEM | Comedy | BOB | FAWCETT |
# | DARES PLUTO | Animation | BOB | FAWCETT |
# | DARN FORRESTER | Action | BOB | FAWCETT |
# | DAZED PUNK | Games | BOB | FAWCETT |
# | DYNAMITE TARZAN | Classics | BOB | FAWCETT |
# | HATE HANDICAP | Comedy | BOB | FAWCETT |
# | HOMICIDE PEACH | Family | BOB | FAWCETT |
# | JACKET FRISCO | Drama | BOB | FAWCETT |
# | JUMANJI BLADE | New | BOB | FAWCETT |
# | LAWLESS VISION | Animation | BOB | FAWCETT |
# | LEATHERNECKS DWARFS | Travel | BOB | FAWCETT |
# | OSCAR GOLD | Animation | BOB | FAWCETT |
# | PELICAN COMFORTS | Documentary | BOB | FAWCETT |
# | PERSONAL LADYBUGS | Music | BOB | FAWCETT |
# | RAGING AIRPLANE | Sci-Fi | BOB | FAWCETT |
# | RUN PACIFIC | New | BOB | FAWCETT |
# | RUNNER MADIGAN | Music | BOB | FAWCETT |
# | SADDLE ANTITRUST | Comedy | BOB | FAWCETT |
# | SCORPION APOLLO | Drama | BOB | FAWCETT |
# | SHAWSHANK BUBBLE | Travel | BOB | FAWCETT |
# | TAXI KICK | Music | BOB | FAWCETT |
# | BERETS AGENT | Action | JULIA | FAWCETT |
# | BOILED DARES | Travel | JULIA | FAWCETT |
# | CHISUM BEHAVIOR | Family | JULIA | FAWCETT |
# | CLOSER BANG | Comedy | JULIA | FAWCETT |
# | DAY UNFAITHFUL | New | JULIA | FAWCETT |
# | HOPE TOOTSIE | Classics | JULIA | FAWCETT |
# | LUKE MUMMY | Animation | JULIA | FAWCETT |
# | MULAN MOON | Comedy | JULIA | FAWCETT |
# | OPUS ICE | Foreign | JULIA | FAWCETT |
# | POLLOCK DELIVERANCE | Foreign | JULIA | FAWCETT |
# | RIDGEMONT SUBMARINE | New | JULIA | FAWCETT |
# | SHANGHAI TYCOON | Travel | JULIA | FAWCETT |
# | SHAWSHANK BUBBLE | Travel | JULIA | FAWCETT |
# | THEORY MERMAID | Animation | JULIA | FAWCETT |
# | WAIT CIDER | Animation | JULIA | FAWCETT |
# +---------------------+---------------+------------+-----------+
# 40 rows in set (0.00 sec)



# Query 31: Create view film_ctgry_actor joining film, category, and actor details
query = """
CREATE VIEW film_ctgry_actor
AS 
SELECT 
 f.title AS title,
 c.name AS category_name,
 a.first_name AS first_name,
 a.last_name  AS last_name 
FROM film f
INNER JOIN film_category fc 
ON fc.film_id = f.film_id
INNER JOIN category c
ON fc.category_id = c.category_id
INNER JOIN film_actor fa
ON fa.film_id = f.film_id
INNER JOIN actor a
ON fa.actor_id = a.actor_id
"""


# Query 32: Select top 5 rows from film_ctgry_actor where actor last name is FAWCETT
query = """
SELECT * 
FROM film_ctgry_actor
WHERE last_name = 'FAWCETT'
LIMIT 5;
"""

# Exercise 14-2
# The film rental company manager would like to have a report that includes the name
# of every country, along with the total payments for all customers who live in each
# country. Generate a view definition that queries the country table and uses a scalar
# subquery to calculate a value for a column named tot_payments.



# Query 33: Create view country_rev aggregating total payments per country
query = """
CREATE VIEW country_rev
AS
SELECT 
 c.country AS country,
 SUM(p.amount) AS tot_payments
FROM country c
INNER JOIN city cc
ON cc.country_id = c.country_id
INNER JOIN address a
ON a.city_id = cc.city_id
INNER JOIN customer cu
ON a.address_id = cu.address_id
INNER JOIN rental r
ON r.customer_id = cu.customer_id
INNER JOIN payment p
ON p.rental_id = r.rental_id
GROUP BY country 
"""



# Query 34: Retrieve top 5 rows from country_rev view
query = """
SELECT *
FROM country_rev
LIMIT 5;
"""

# Execute query
results = executor.execute_query(query)


print(results)
executor.close()