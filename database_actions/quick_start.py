"""
Quick Start Script for MSSQL CRUD Operations
===========================================
Author: System Assistant
Date: April 13, 2026

This script helps you quickly test database connectivity and basic CRUD operations.
Run this script to verify your setup before using the full framework.
"""

import sys
import os
from typing import Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from mssql_crud_framework import MSSQLCrudFramework
    from database_config import DatabaseConfig, print_available_drivers
    import pandas as pd
    import pyodbc
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Please install required packages:")
    print("pip install pandas pyodbc sqlalchemy numpy")
    sys.exit(1)

def test_package_installation():
    """Test if all required packages are properly installed."""
    
    print("🧪 Testing Package Installation")
    print("-" * 30)
    
    required_packages = {
        'pandas': pd.__version__,
        'pyodbc': pyodbc.version,
        'sqlalchemy': None
    }
    
    try:
        import sqlalchemy
        required_packages['sqlalchemy'] = sqlalchemy.__version__
    except ImportError:
        pass
    
    try:
        import numpy as np
        required_packages['numpy'] = np.__version__
    except ImportError:
        pass
    
    print("📦 Installed packages:")
    for package, version in required_packages.items():
        if version:
            print(f"   ✅ {package}: {version}")
        else:
            print(f"   ❌ {package}: Not installed")
    
    print("\n🔧 Available ODBC drivers:")
    print_available_drivers()
    
    return all(required_packages.values())

def get_user_database_config() -> Optional[DatabaseConfig]:
    """
    Interactive database configuration setup.
    
    Returns:
        DatabaseConfig or None if setup failed
    """
    
    print("\n⚙️ Database Configuration Setup")
    print("-" * 30)
    
    try:
        print("Please provide your database connection details:")
        
        # Get server name
        server = input("📍 Server name (e.g., localhost, localhost\\SQLEXPRESS): ").strip()
        if not server:
            server = "localhost"
            
        # Get database name
        database = input("🗃️ Database name (e.g., TestDB, master): ").strip()
        if not database:
            database = "master"  # Use master as default for testing
        
        # Authentication method
        print("\n🔐 Authentication method:")
        print("1. Windows Authentication (recommended for local)")
        print("2. SQL Server Authentication")
        
        auth_choice = input("Choose (1 or 2, default=1): ").strip()
        
        if auth_choice == "2":
            username = input("👤 Username: ").strip()
            password = input("🔑 Password: ").strip()
            trusted_connection = False
        else:
            username = None
            password = None 
            trusted_connection = True
        
        # ODBC Driver
        driver = input("🚗 ODBC Driver (press Enter for default): ").strip()
        if not driver:
            driver = "ODBC Driver 17 for SQL Server"
        
        config = DatabaseConfig(
            server=server,
            database=database,
            username=username,
            password=password,
            trusted_connection=trusted_connection,
            driver=driver
        )
        
        print(f"\n📋 Configuration Summary:")
        print(f"   Server: {config.server}")
        print(f"   Database: {config.database}")
        print(f"   Authentication: {'Windows' if config.trusted_connection else 'SQL Server'}")
        print(f"   Driver: {config.driver}")
        
        return config
        
    except KeyboardInterrupt:
        print("\n⏹️ Setup cancelled by user")
        return None
    except Exception as e:
        print(f"\n❌ Configuration setup failed: {str(e)}")
        return None

def test_database_connection(config: DatabaseConfig) -> bool:
    """
    Test database connectivity with the provided configuration.
    
    Args:
        config: Database configuration to test
        
    Returns:
        bool: True if connection successful
    """
    
    print("\n🔌 Testing Database Connection")
    print("-" * 30)
    
    try:
        with MSSQLCrudFramework(
            server=config.server,
            database=config.database,
            username=config.username,
            password=config.password,
            trusted_connection=config.trusted_connection,
            driver=config.driver
        ) as crud:
            
            # Test connections
            connection_status = crud.test_connection()
            
            print("📊 Connection Test Results:")
            for method, status in connection_status.items():
                status_icon = "✅" if status else "❌"
                print(f"   {status_icon} {method}: {'Connected' if status else 'Failed'}")
            
            if all(connection_status.values()):
                print("\n🎉 All connections successful!")
                return True
            else:
                print("\n⚠️ Some connections failed. Check your configuration.")
                return False
                
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        print("\nCommon solutions:")
        print("• Check if SQL Server is running")
        print("• Verify server name and database exist")
        print("• Ensure you have database access permissions")
        print("• Check Windows firewall settings")
        return False

def test_basic_operations(config: DatabaseConfig) -> bool:
    """
    Test basic CRUD operations on a system table.
    
    Args:
        config: Database configuration
        
    Returns:
        bool: True if operations successful
    """
    
    print("\n🧪 Testing Basic Operations")
    print("-" * 30)
    
    try:
        with MSSQLCrudFramework(
            server=config.server,
            database=config.database,
            username=config.username,
            password=config.password,
            trusted_connection=config.trusted_connection,
            driver=config.driver
        ) as crud:
            
            # Test 1: Query system information
            print("📊 Test 1: Reading system information...")
            
            system_query = """
            SELECT 
                @@VERSION as sql_version,
                @@SERVERNAME as server_name,
                DB_NAME() as current_database,
                SYSTEM_USER as current_user,
                GETDATE() as current_datetime
            """
            
            system_info = crud.read_query(system_query)
            print("   ✅ System query successful")
            print(f"   🖥️ Server: {system_info['server_name'][0]}")
            print(f"   🗃️ Database: {system_info['current_database'][0]}")
            print(f"   👤 User: {system_info['current_user'][0]}")
            
            # Test 2: List tables in database
            print("\n📊 Test 2: Listing database tables...")
            
            tables_query = """
            SELECT 
                TABLE_SCHEMA,
                TABLE_NAME,
                TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            ORDER BY TABLE_SCHEMA, TABLE_NAME
            """
            
            tables_df = crud.read_query(tables_query)
            print(f"   ✅ Found {len(tables_df)} tables/views")
            
            if len(tables_df) > 0:
                print("   📋 Sample tables:")
                for i, row in tables_df.head(5).iterrows():
                    print(f"      • {row['TABLE_SCHEMA']}.{row['TABLE_NAME']} ({row['TABLE_TYPE']})")
            
            # Test 3: Test a simple table read (if any user tables exist)
            user_tables = tables_df[
                (tables_df['TABLE_TYPE'] == 'BASE TABLE') & 
                (tables_df['TABLE_SCHEMA'] == 'dbo')
            ]
            
            if len(user_tables) > 0:
                sample_table = user_tables.iloc[0]['TABLE_NAME']
                print(f"\n📊 Test 3: Reading sample data from {sample_table}...")
                
                try:
                    sample_data = crud.read_table(sample_table, limit=5)
                    print(f"   ✅ Successfully read {len(sample_data)} rows")
                    print(f"   📊 Columns: {list(sample_data.columns)}")
                except Exception as e:
                    print(f"   ⚠️ Could not read table data: {str(e)}")
            else:
                print("\n📊 Test 3: Skipped (no user tables found)")
            
            print("\n🎉 Basic operations completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Basic operations test failed: {str(e)}")
        return False

def create_test_table_demo(config: DatabaseConfig) -> bool:
    """
    Create and test operations on a temporary test table.
    
    Args:
        config: Database configuration
        
    Returns:
        bool: True if demo successful
    """
    
    print("\n🎯 Create Test Table Demo")
    print("-" * 30)
    
    try:
        with MSSQLCrudFramework(
            server=config.server,
            database=config.database,
            username=config.username,
            password=config.password,
            trusted_connection=config.trusted_connection,
            driver=config.driver
        ) as crud:
            
            # Create test table
            print("📝 Creating test table...")
            
            create_table_sql = """
            IF EXISTS (SELECT * FROM sysobjects WHERE name='quick_test_table' AND xtype='U')
                DROP TABLE quick_test_table;
            
            CREATE TABLE quick_test_table (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(50) NOT NULL,
                value FLOAT,
                created_at DATETIME2 DEFAULT GETDATE()
            );
            """
            
            crud.sqlalchemy_session.execute(crud.sqlalchemy_engine.text(create_table_sql))
            crud.sqlalchemy_session.commit()
            print("   ✅ Test table created")
            
            # Insert test data
            print("\n📥 Inserting test data...")
            
            test_data = pd.DataFrame({
                'name': ['Test1', 'Test2', 'Test3'],
                'value': [10.5, 20.7, 30.9]
            })
            
            crud.insert_dataframe(test_data, 'quick_test_table')
            print("   ✅ Test data inserted")
            
            # Read test data
            print("\n📤 Reading test data...")
            
            result_df = crud.read_table('quick_test_table')
            print(f"   ✅ Retrieved {len(result_df)} records")
            print("   📊 Sample data:")
            print(result_df.to_string(index=False))
            
            # Update test data
            print("\n🔄 Updating test data...")
            
            rows_updated = crud.update_records(
                table_name='quick_test_table',
                set_values={'value': 99.9},
                conditions={'name': 'Test1'}
            )
            print(f"   ✅ Updated {rows_updated} record(s)")
            
            # Delete test data  
            print("\n🗑️ Cleaning up...")
            
            crud.sqlalchemy_session.execute(crud.sqlalchemy_engine.text("DROP TABLE quick_test_table"))
            crud.sqlalchemy_session.commit()
            print("   ✅ Test table dropped")
            
            print("\n🎉 Test table demo completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Test table demo failed: {str(e)}")
        print("Note: This might be due to insufficient permissions to create tables.")
        return False

def main():
    """Main quick start function."""
    
    print("🚀 MSSQL CRUD Framework - Quick Start")
    print("=" * 50)
    
    # Test package installation
    if not test_package_installation():
        print("\n❌ Package installation incomplete. Please install missing packages.")
        return False
    
    # Get database configuration
    config = get_user_database_config()
    if not config:
        print("\n❌ Database configuration failed.")
        return False
    
    # Test database connection
    if not test_database_connection(config):
        print("\n❌ Database connection failed. Please check your configuration.")
        return False
    
    # Test basic operations
    if not test_basic_operations(config):
        print("\n❌ Basic operations failed.")
        return False
    
    # Ask if user wants to run table demo
    print("\n🎯 Would you like to run a test table demo?")
    print("   (This will create and drop a temporary table)")
    
    run_demo = input("Run demo? (y/N): ").strip().lower()
    
    if run_demo in ['y', 'yes']:
        create_test_table_demo(config)
    
    # Final success message
    print("\n" + "=" * 50)
    print("🎉 Quick start completed successfully!")
    print("\nNext steps:")
    print("• Run the full examples: python crud_examples_and_tests.py")
    print("• Read the documentation: README.md")
    print("• Explore the framework capabilities")
    print("• Adapt the configuration for your specific needs")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Quick start failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Quick start cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)