from execute_sql import main


executor = main()


###############
# learning sql by alan beaulieu - Chapter - 15
###############




# Query 1: List all tables and their types in the sakila schema
query = """
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'sakila'
ORDER BY 1;
"""



# Query 2: List only base tables in the sakila schema
query = """
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'sakila'
AND table_type = 'BASE TABLE'
ORDER BY 1;
"""



# Query 3: List only view objects in the sakila schema
query = """
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'sakila'
AND table_type = 'VIEW'
ORDER BY 1;
"""



# Query 4: List views and whether they are updatable in the sakila schema
query = """
SELECT table_name, is_updatable
FROM information_schema.views
WHERE table_schema = 'sakila'
ORDER BY 1;
"""



# Query 5: Show first five columns of the 'film' table
query = """
SELECT *
FROM information_schema.columns
WHERE table_schema = 'sakila'
AND table_name = 'film'
LIMIT 5
"""



# Query 6: Show first five index statistics for the 'rental' table
query = """
SELECT *
FROM information_schema.statistics
WHERE table_schema = 'sakila'
AND table_name = 'rental'
LIMIT 5
"""



# Query 7: List first five table constraints in the sakila schema
query = """
SELECT *
FROM information_schema.table_constraints
WHERE table_schema = 'sakila'
LIMIT 5
"""

# Execute query
results = executor.execute_query(query)


print(results)
executor.close()