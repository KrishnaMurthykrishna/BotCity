"""
Universal Open Source Database CRUD Framework  
===========================================
Author: System Assistant
Date: April 13, 2026

Universal CRUD framework supporting multiple open source databases:
- SQLite: No server required, file-based
- PostgreSQL: Popular open source database  
- MySQL/MariaDB: Widely used open source database
- Supports free cloud database services
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Optional, Any, Union
import logging
import os
from datetime import datetime
import traceback

# Import our open source database configurations
try:
    from opensource_db_config import (
        OpenSourceDBConfig, 
        get_sqlalchemy_url,
        SQLITE_CONFIGS,
        POSTGRESQL_CLOUD_CONFIGS,
        MYSQL_CONFIGS,
        setup_sqlite_database,
        setup_memory_database
    )
except ImportError:
    print("⚠️ Could not import opensource_db_config. Make sure the file exists.")

class UniversalCrudFramework:
    """
    Universal CRUD operations framework for open source databases.
    
    Supports:
    - SQLite (file-based, no server needed)
    - PostgreSQL (local or cloud)
    - MySQL/MariaDB (local or cloud)
    
    Features:
    - Full CRUD operations with pandas integration
    - Professional logging and error handling  
    - Multiple database support with unified API
    - Free cloud database service support
    """
    
    def __init__(self, config: OpenSourceDBConfig, echo: bool = False):
        """
        Initialize Universal CRUD Framework.
        
        Args:
            config (OpenSourceDBConfig): Database configuration
            echo (bool): Enable SQL query logging
        """
        self.config = config
        self.db_type = config.db_type
        self.echo = echo
        
        # Initialize connections
        self.engine = None
        self.session = None
        self.metadata = None
        
        # Setup logging
        self.setup_logging()
        
        # Connect to database
        self.connect_database()
    
    def setup_logging(self) -> None:
        """Setup comprehensive logging system."""
        try:
            # Create logs directory
            logs_dir = os.path.join(os.getcwd(), 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            
            # Configure logging
            log_filename = f"universal_crud_{self.db_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_filepath = os.path.join(logs_dir, log_filename)
            
            # Configure logging if not already configured
            if not logging.getLogger().handlers:
                logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_filepath, encoding='utf-8'),
                        logging.StreamHandler()
                    ]
                )
            
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"🚀 Universal CRUD Framework initialized for {self.db_type.upper()}")
            
        except Exception as e:
            # Fallback to basic logging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
            self.logger.warning(f"⚠️ Advanced logging setup failed, using basic logging: {str(e)}")
    
    def connect_database(self) -> None:
        """Establish database connection using SQLAlchemy."""
        try:
            # Build connection URL
            connection_url = get_sqlalchemy_url(self.config)
            
            # Create engine
            self.engine = create_engine(connection_url, echo=self.echo)
            
            # Create session
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            
            # Create metadata
            self.metadata = MetaData()
            
            self.logger.info(f"✅ {self.db_type.upper()} connection established")
            
            # For SQLite, create directory if needed
            if self.db_type == "sqlite" and self.config.database != ":memory:":
                db_dir = os.path.dirname(os.path.abspath(self.config.database))
                os.makedirs(db_dir, exist_ok=True)
                self.logger.info(f"📁 SQLite database: {os.path.abspath(self.config.database)}")
            
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise
    
    # ==========================================
    # READ OPERATIONS
    # ==========================================
    
    def read_table(self, table_name: str, schema: Optional[str] = None, 
                   limit: Optional[int] = None) -> pd.DataFrame:
        """
        Read entire table into pandas DataFrame.
        
        Args:
            table_name (str): Name of the table to read
            schema (Optional[str]): Schema name (PostgreSQL/MySQL only)
            limit (Optional[int]): Limit number of rows
            
        Returns:
            pd.DataFrame: Table data as pandas DataFrame
        """
        try:
            # Build table reference
            if schema and self.db_type in ["postgresql", "mysql"]:
                table_ref = f'"{schema}"."{table_name}"' if self.db_type == "postgresql" else f"`{schema}`.`{table_name}`"
            else:
                table_ref = f'"{table_name}"' if self.db_type == "postgresql" else f"`{table_name}`" if self.db_type == "mysql" else table_name
            
            query = f"SELECT * FROM {table_ref}"
            
            if limit:
                if self.db_type == "mysql":
                    query += f" LIMIT {limit}"
                else:  # PostgreSQL and SQLite
                    query += f" LIMIT {limit}"
            
            df = pd.read_sql(query, self.engine)
            self.logger.info(f"📊 Successfully read {len(df)} rows from {table_name}")
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Failed to read table {table_name}: {str(e)}")
            raise
    
    def read_query(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Execute custom SQL query and return pandas DataFrame.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Dict]): Query parameters
            
        Returns:
            pd.DataFrame: Query results as pandas DataFrame
        """
        try:
            if params:
                df = pd.read_sql(query, self.engine, params=params)
            else:
                df = pd.read_sql(query, self.engine)
            
            self.logger.info(f"📊 Query executed successfully, returned {len(df)} rows")
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Query execution failed: {str(e)}")
            self.logger.error(f"Query: {query}")
            raise
    
    def read_with_conditions(self, table_name: str, conditions: Dict[str, Any],
                           schema: Optional[str] = None, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Read table with WHERE clause conditions.
        
        Args:
            table_name (str): Name of the table
            conditions (Dict[str, Any]): Column-value pairs for WHERE clause
            schema (Optional[str]): Schema name
            columns (Optional[List[str]]): Specific columns to select
            
        Returns:
            pd.DataFrame: Filtered data
        """
        try:
            # Build column list
            if columns:
                if self.db_type == "postgresql":
                    col_list = ", ".join([f'"{col}"' for col in columns])
                elif self.db_type == "mysql":
                    col_list = ", ".join([f"`{col}`" for col in columns])
                else:  # SQLite
                    col_list = ", ".join(columns)
            else:
                col_list = "*"
            
            # Build table reference
            if schema and self.db_type in ["postgresql", "mysql"]:
                table_ref = f'"{schema}"."{table_name}"' if self.db_type == "postgresql" else f"`{schema}`.`{table_name}`"
            else:
                table_ref = f'"{table_name}"' if self.db_type == "postgresql" else f"`{table_name}`" if self.db_type == "mysql" else table_name
            
            # Build WHERE clause
            where_parts = []
            params = {}
            for i, (key, value) in enumerate(conditions.items()):
                param_name = f"param_{i}"
                if self.db_type == "postgresql":
                    where_parts.append(f'"{key}" = %({param_name})s')
                elif self.db_type == "mysql":
                    where_parts.append(f"`{key}` = %({param_name})s")
                else:  # SQLite
                    where_parts.append(f"{key} = :{param_name}")
                params[param_name] = value
            
            where_clause = " AND ".join(where_parts)
            query = f"SELECT {col_list} FROM {table_ref} WHERE {where_clause}"
            
            df = pd.read_sql(query, self.engine, params=params)
            self.logger.info(f"📊 Read {len(df)} rows from {table_name} with conditions")
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Conditional read failed: {str(e)}")
            raise
    
    # ==========================================
    # CREATE/INSERT OPERATIONS
    # ==========================================
    
    def insert_dataframe(self, df: pd.DataFrame, table_name: str, 
                        schema: Optional[str] = None, if_exists: str = "append",
                        index: bool = False, method: Optional[str] = "multi") -> bool:
        """
        Insert pandas DataFrame to SQL table using to_sql.
        
        Args:
            df (pd.DataFrame): Data to insert
            table_name (str): Target table name
            schema (Optional[str]): Schema name
            if_exists (str): Action if table exists ('fail', 'replace', 'append')
            index (bool): Include DataFrame index
            method (Optional[str]): Insert method
            
        Returns:
            bool: Success status
        """
        try:
            # For SQLite, schema parameter should be None
            actual_schema = schema if self.db_type in ["postgresql", "mysql"] else None
            
            df.to_sql(
                name=table_name,
                con=self.engine,
                schema=actual_schema,
                if_exists=if_exists,
                index=index,
                method=method
            )
            
            schema_info = f"{schema}." if actual_schema else ""
            self.logger.info(f"✅ Successfully inserted {len(df)} rows into {schema_info}{table_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Insert operation failed: {str(e)}")
            raise
    
    def insert_records(self, table_name: str, records: List[Dict[str, Any]],
                      schema: Optional[str] = None) -> bool:
        """
        Insert multiple records using pandas DataFrame.
        
        Args:
            table_name (str): Target table name
            records (List[Dict[str, Any]]): List of record dictionaries
            schema (Optional[str]): Schema name
            
        Returns:
            bool: Success status
        """
        try:
            # Convert to DataFrame and use to_sql
            df = pd.DataFrame(records)
            return self.insert_dataframe(df, table_name, schema)
            
        except Exception as e:
            self.logger.error(f"❌ Record insert failed: {str(e)}")
            raise
    
    def bulk_insert_csv(self, csv_file_path: str, table_name: str,
                       schema: Optional[str] = None, **pandas_kwargs) -> bool:
        """
        Bulk insert data from CSV file.
        
        Args:
            csv_file_path (str): Path to CSV file
            table_name (str): Target table name
            schema (Optional[str]): Schema name
            **pandas_kwargs: Additional arguments for pd.read_csv
            
        Returns:
            bool: Success status
        """
        try:
            # Read CSV file
            df = pd.read_csv(csv_file_path, **pandas_kwargs)
            self.logger.info(f"📁 Loaded {len(df)} rows from {csv_file_path}")
            
            # Insert to database
            return self.insert_dataframe(df, table_name, schema)
            
        except Exception as e:
            self.logger.error(f"❌ CSV bulk insert failed: {str(e)}")
            raise
    
    # ==========================================
    # UPDATE OPERATIONS  
    # ==========================================
    
    def update_records(self, table_name: str, set_values: Dict[str, Any],
                      conditions: Dict[str, Any], schema: Optional[str] = None) -> int:
        """
        Update records using SQLAlchemy.
        
        Args:
            table_name (str): Target table name
            set_values (Dict[str, Any]): Column-value pairs to update
            conditions (Dict[str, Any]): WHERE clause conditions
            schema (Optional[str]): Schema name
            
        Returns:
            int: Number of rows affected
        """
        try:
            # Build table reference
            if schema and self.db_type in ["postgresql", "mysql"]:
                table_ref = f'"{schema}"."{table_name}"' if self.db_type == "postgresql" else f"`{schema}`.`{table_name}`"
            else:
                table_ref = f'"{table_name}"' if self.db_type == "postgresql" else f"`{table_name}`" if self.db_type == "mysql" else table_name
            
            # Build SET clause
            set_parts = []
            params = {}
            for i, (key, value) in enumerate(set_values.items()):
                param_name = f"set_param_{i}"
                if self.db_type == "postgresql":
                    set_parts.append(f'"{key}" = %({param_name})s')
                elif self.db_type == "mysql":
                    set_parts.append(f"`{key}` = %({param_name})s")
                else:  # SQLite
                    set_parts.append(f"{key} = :{param_name}")
                params[param_name] = value
            
            # Build WHERE clause
            where_parts = []
            for i, (key, value) in enumerate(conditions.items()):
                param_name = f"where_param_{i}"
                if self.db_type == "postgresql":
                    where_parts.append(f'"{key}" = %({param_name})s')
                elif self.db_type == "mysql":
                    where_parts.append(f"`{key}` = %({param_name})s")
                else:  # SQLite
                    where_parts.append(f"{key} = :{param_name}")
                params[param_name] = value
            
            set_clause = ", ".join(set_parts)
            where_clause = " AND ".join(where_parts)
            
            query = f"UPDATE {table_ref} SET {set_clause} WHERE {where_clause}"
            
            result = self.session.execute(text(query), params)
            self.session.commit()
            
            rows_affected = result.rowcount
            schema_info = f"{schema}." if schema else ""
            self.logger.info(f"✅ Updated {rows_affected} rows in {schema_info}{table_name}")
            return rows_affected
            
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"❌ Update operation failed: {str(e)}")
            raise
    
    # ==========================================
    # DELETE OPERATIONS
    # ==========================================
    
    def delete_records(self, table_name: str, conditions: Dict[str, Any],
                      schema: Optional[str] = None) -> int:
        """
        Delete records based on conditions.
        
        Args:
            table_name (str): Target table name
            conditions (Dict[str, Any]): WHERE clause conditions
            schema (Optional[str]): Schema name
            
        Returns:
            int: Number of rows deleted
        """
        try:
            # Build table reference
            if schema and self.db_type in ["postgresql", "mysql"]:
                table_ref = f'"{schema}"."{table_name}"' if self.db_type == "postgresql" else f"`{schema}`.`{table_name}`"
            else:
                table_ref = f'"{table_name}"' if self.db_type == "postgresql" else f"`{table_name}`" if self.db_type == "mysql" else table_name
            
            # Build WHERE clause
            where_parts = []
            params = {}
            for i, (key, value) in enumerate(conditions.items()):
                param_name = f"param_{i}"
                if self.db_type == "postgresql":
                    where_parts.append(f'"{key}" = %({param_name})s')
                elif self.db_type == "mysql":
                    where_parts.append(f"`{key}` = %({param_name})s")
                else:  # SQLite
                    where_parts.append(f"{key} = :{param_name}")
                params[param_name] = value
            
            where_clause = " AND ".join(where_parts)
            query = f"DELETE FROM {table_ref} WHERE {where_clause}"
            
            result = self.session.execute(text(query), params)
            self.session.commit()
            
            rows_affected = result.rowcount
            schema_info = f"{schema}." if schema else ""
            self.logger.info(f"🗑️ Deleted {rows_affected} rows from {schema_info}{table_name}")
            return rows_affected
            
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"❌ Delete operation failed: {str(e)}")
            raise
    
    # ==========================================
    # UTILITY OPERATIONS
    # ==========================================
    
    def get_table_info(self, table_name: str, schema: Optional[str] = None) -> pd.DataFrame:
        """
        Get table structure information.
        
        Args:
            table_name (str): Table name
            schema (Optional[str]): Schema name
            
        Returns:
            pd.DataFrame: Table column information
        """
        try:
            inspector = inspect(self.engine)
            
            # Get columns information
            if schema and self.db_type in ["postgresql", "mysql"]:
                columns = inspector.get_columns(table_name, schema=schema)
            else:
                columns = inspector.get_columns(table_name)
            
            # Convert to DataFrame
            columns_data = []
            for col in columns:
                columns_data.append({
                    'column_name': col['name'],
                    'data_type': str(col['type']),
                    'nullable': col['nullable'],
                    'default': col['default'],
                    'primary_key': col.get('primary_key', False)
                })
            
            df = pd.DataFrame(columns_data)
            schema_info = f"{schema}." if schema else ""
            self.logger.info(f"📋 Retrieved structure info for {schema_info}{table_name}")
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get table info: {str(e)}")
            raise
    
    def get_row_count(self, table_name: str, schema: Optional[str] = None,
                     conditions: Optional[Dict[str, Any]] = None) -> int:
        """
        Get row count for table with optional conditions.
        
        Args:
            table_name (str): Table name
            schema (Optional[str]): Schema name
            conditions (Optional[Dict[str, Any]]): WHERE clause conditions
            
        Returns:
            int: Row count
        """
        try:
            # Build table reference
            if schema and self.db_type in ["postgresql", "mysql"]:
                table_ref = f'"{schema}"."{table_name}"' if self.db_type == "postgresql" else f"`{schema}`.`{table_name}`"
            else:
                table_ref = f'"{table_name}"' if self.db_type == "postgresql" else f"`{table_name}`" if self.db_type == "mysql" else table_name
            
            query = f"SELECT COUNT(*) as row_count FROM {table_ref}"
            params = {}
            
            if conditions:
                where_parts = []
                for i, (key, value) in enumerate(conditions.items()):
                    param_name = f"param_{i}"
                    if self.db_type == "postgresql":
                        where_parts.append(f'"{key}" = %({param_name})s')
                    elif self.db_type == "mysql":
                        where_parts.append(f"`{key}` = %({param_name})s")
                    else:  # SQLite
                        where_parts.append(f"{key} = :{param_name}")
                    params[param_name] = value
                
                query += f" WHERE {' AND '.join(where_parts)}"
            
            result = pd.read_sql(query, self.engine, params=params)
            count = result['row_count'].iloc[0]
            
            schema_info = f"{schema}." if schema else ""
            self.logger.info(f"📊 Row count for {schema_info}{table_name}: {count}")
            return count
            
        except Exception as e:
            self.logger.error(f"❌ Row count failed: {str(e)}")
            raise
    
    def list_tables(self, schema: Optional[str] = None) -> List[str]:
        """
        List all tables in the database.
        
        Args:
            schema (Optional[str]): Schema name to filter by
            
        Returns:
            List[str]: List of table names
        """
        try:
            inspector = inspect(self.engine)
            
            if schema and self.db_type in ["postgresql", "mysql"]:
                tables = inspector.get_table_names(schema=schema)
            else:
                tables = inspector.get_table_names()
            
            self.logger.info(f"📋 Found {len(tables)} tables")
            return tables
            
        except Exception as e:
            self.logger.error(f"❌ Failed to list tables: {str(e)}")
            raise
    
    # ==========================================
    # CONNECTION MANAGEMENT
    # ==========================================
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            bool: Connection status  
        """
        try:
            # Simple test query appropriate for each database type
            if self.db_type == "sqlite":
                test_query = "SELECT 1"
            elif self.db_type == "postgresql":
                test_query = "SELECT 1"
            elif self.db_type == "mysql":
                test_query = "SELECT 1"
            else:
                test_query = "SELECT 1"
            
            result = self.session.execute(text(test_query))
            result.fetchone()
            
            self.logger.info(f"✅ {self.db_type.upper()} connection test successful")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ {self.db_type.upper()} connection test failed: {str(e)}")
            return False
    
    def close_connections(self) -> None:
        """Close all database connections."""
        try:
            if self.session:
                self.session.close()
                self.logger.info("🔒 Database session closed")
            
            if self.engine:
                self.engine.dispose()
                self.logger.info("🔒 Database engine disposed")
                
        except Exception as e:
            self.logger.error(f"⚠️ Error closing connections: {str(e)}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_connections()

# ==========================================
# CONVENIENCE FUNCTIONS
# ==========================================

def create_sqlite_crud(db_file: str = "database.db") -> UniversalCrudFramework:
    """
    Create CRUD framework for SQLite database.
    
    Args:
        db_file (str): SQLite database file path
        
    Returns:
        UniversalCrudFramework: CRUD framework instance
    """
    config = setup_sqlite_database(db_file)
    return UniversalCrudFramework(config)

def create_memory_crud() -> UniversalCrudFramework:
    """
    Create CRUD framework for in-memory SQLite database.
    
    Returns:
        UniversalCrudFramework: CRUD framework instance
    """
    config = setup_memory_database()
    return UniversalCrudFramework(config)