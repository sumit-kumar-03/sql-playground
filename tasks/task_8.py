from execute_sql import main


executor = main()


query ="""
SELECT DISTINCT first_name
FROM customer
LIMIT 100;
"""


# Execute query
results = executor.execute_query(query)


print(results)
executor.close()