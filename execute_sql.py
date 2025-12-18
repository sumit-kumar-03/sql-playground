#!/usr/bin/env python3
"""
MySQL Query Executor
Execute SQL queries against the MySQL database running in Docker.
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Tuple, Optional


class MySQLExecutor:
    """MySQL database connection and query executor."""
    
    def __init__(self, host='localhost', port=3306, user='root', password='example', database='sakila'):
        """
        Initialize MySQL connection parameters.
        
        Args:
            host: MySQL host (default: localhost)
            port: MySQL port (default: 3306)
            user: MySQL user (default: root)
            password: MySQL password (default: example)
            database: Database name (default: sakila)
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """Establish connection to MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                consume_results=True
            )
            if self.connection.is_connected():
                db_info = self.connection.server_info
                print(f"✅ Connected to MySQL Server version {db_info}")
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT DATABASE();")
                    record = cursor.fetchone()
                    print(f"✅ Connected to database: {record[0]}")
                return True
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Optional[List[Tuple]]:
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query string
            params: Optional tuple of parameters for parameterized queries
            
        Returns:
            List of tuples containing query results, or None if error
        """
        if not self.connection or not self.connection.is_connected():
            print("❌ Not connected to database. Call connect() first.")
            return None
        
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            
            # Check if it's a query that returns results
            query_upper = query.strip().upper()
            returns_results = query_upper.startswith(('SELECT', 'SHOW', 'DESCRIBE', 'DESC', 'EXPLAIN'))
            
            if returns_results:
                results = cursor.fetchall()
                print(f"✅ Query executed successfully. {len(results)} rows returned.")
                
                # Print column names
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    print(f"\nColumns: {', '.join(columns)}")
                
                cursor.close()
                return results
            else:
                # For INSERT, UPDATE, DELETE queries
                self.connection.commit()
                print(f"✅ Query executed successfully. {cursor.rowcount} rows affected.")
                cursor.close()
                return None
                
        except Error as e:
            print(f"❌ Error executing query: {e}")
            return None
    
    
    def execute_file(self, filepath: str) -> bool:
        """
        Execute SQL commands from a file.
        
        Args:
            filepath: Path to SQL file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'r') as file:
                sql_script = file.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            
            for statement in statements:
                self.execute_query(statement)
            
            print(f"✅ Executed {len(statements)} statements from {filepath}")
            return True
            
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            return False
        except Exception as e:
            print(f"❌ Error executing file: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ MySQL connection closed")


def main():
    """Example usage of MySQLExecutor."""
    
    # Create executor instance
    executor = MySQLExecutor(
        host='localhost',
        port=3306,
        user='root',
        password='example',
        database='sakila'
    )
    
    # Connect to database
    if not executor.connect():
        return

    return executor

