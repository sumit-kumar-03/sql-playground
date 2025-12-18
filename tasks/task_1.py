
from execute_sql import main


executor = main()


# Show all databases
query = "SHOW DATABASES;"


query ="SHOW TABLES;"

# Execute query
results = executor.execute_query(query)

print(results)

executor.close()
