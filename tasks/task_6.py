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
# index and constraints by alan beaulieu - Chapter - 13
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


# Execute query
results = executor.execute_query(query)


print(results)
executor.close()