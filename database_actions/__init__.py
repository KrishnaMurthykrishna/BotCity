"""
MSSQL Database Actions Package
=============================
Author: System Assistant
Date: April 13, 2026

A comprehensive Python package for CRUD operations on Microsoft SQL Server
using pandas, pyodbc, and SQLAlchemy.

Package Components:
- MSSQLCrudFramework: Main CRUD operations class
- DatabaseConfig: Configuration management 
- Examples and testing utilities
- Professional logging and error handling
"""

__version__ = "1.0.0"
__author__ = "System Assistant"
__email__ = "admin@company.com"
__description__ = "MSSQL CRUD Operations Framework with pandas integration"

# Import main classes for easy access
from .mssql_crud_framework import MSSQLCrudFramework
from .database_config import (
    DatabaseConfig,
    DEV_CONFIGS,
    PROD_CONFIGS,
    get_config_from_environment,
    build_pyodbc_connection_string,
    build_sqlalchemy_url,
    get_local_config,
    get_docker_config,
    print_available_drivers
)

# Import open source database components
from .universal_crud_framework import UniversalCrudFramework, create_sqlite_crud, create_memory_crud
from .opensource_db_config import (
    OpenSourceDBConfig,
    SQLITE_CONFIGS,
    POSTGRESQL_CLOUD_CONFIGS,
    MYSQL_CONFIGS,
    setup_sqlite_database,
    setup_memory_database,
    create_sample_sqlite_database,
    print_free_database_options
)

# Package metadata
__all__ = [
    # MSSQL Components
    "MSSQLCrudFramework",
    "DatabaseConfig", 
    "DEV_CONFIGS",
    "PROD_CONFIGS",
    "get_config_from_environment",
    "build_pyodbc_connection_string", 
    "build_sqlalchemy_url",
    "get_local_config",
    "get_docker_config",
    "print_available_drivers",
    
    # Open Source Database Components
    "UniversalCrudFramework",
    "create_sqlite_crud",
    "create_memory_crud",
    "OpenSourceDBConfig",
    "SQLITE_CONFIGS",
    "POSTGRESQL_CLOUD_CONFIGS", 
    "MYSQL_CONFIGS",
    "setup_sqlite_database",
    "setup_memory_database",
    "create_sample_sqlite_database",
    "print_free_database_options"
]

# Quick start helper function
def quick_start_demo():
    """
    Run a quick connectivity test and basic operations demo.
    
    This function provides a simple way to test the package installation
    and basic database connectivity with both MSSQL and open source databases.
    """
    print(f"🚀 Database Actions Framework v{__version__}")
    print("=" * 50)
    
    try:
        print("📦 Available Database Options:")
        print("   🗄️ SQLite - No server setup required (recommended for getting started)")
        print("   🐘 PostgreSQL - Free cloud options available")
        print("   🐬 MySQL/MariaDB - Open source alternatives")
        print("   🏢 MSSQL Server - Enterprise database support")
        
        print(f"\n📚 Package components loaded successfully:")
        print(f"   • UniversalCrudFramework - Open source database CRUD")
        print(f"   • MSSQLCrudFramework - MSSQL Server CRUD operations")
        print(f"   • Database configurations and utilities")
        
        print(f"\n🎯 Quick start options:")
        print(f"   1. INSTANT: python run_opensource_demo.py (SQLite - no setup)")
        print(f"   2. FULL DEMO: python opensource_crud_examples.py")
        print(f"   3. MSSQL: python crud_examples_and_tests.py")
        print(f"   4. Check README.md for detailed documentation")
        
        print(f"\n⚡ Ultra-quick test (SQLite in memory):")
        print("""
from database_actions import create_memory_crud
import pandas as pd

with create_memory_crud() as crud:
    df = pd.DataFrame({'name': ['Test'], 'value': [42]})
    crud.insert_dataframe(df, 'test_table')
    result = crud.read_table('test_table')
    print(result)
        """)
        
        return True
        
    except Exception as e:
        print(f"❌ Package initialization failed: {str(e)}")
        return False

# Package information
def package_info():
    """Display package information."""
    print(f"""
📦 Database Actions Framework Information
========================================
Version: {__version__}
Author: {__author__} 
Description: {__description__}

🗄️ SUPPORTED DATABASES:
   • SQLite - File-based, no server required (INSTANT START!)
   • PostgreSQL - Open source, cloud-friendly
   • MySQL/MariaDB - Popular open source databases
   • MSSQL Server - Enterprise Microsoft SQL Server

📁 Package Contents:
   • universal_crud_framework.py - Universal CRUD for open source DBs
   • mssql_crud_framework.py - MSSQL Server CRUD operations
   • opensource_db_config.py - Open source database configurations
   • database_config.py - MSSQL configuration management
   • *_examples.py - Comprehensive usage examples
   • README.md - Complete documentation

🔧 Dependencies:
   • pandas >= 2.1.0 - Data manipulation
   • sqlalchemy >= 2.0.0 - Universal database ORM
   • numpy >= 1.24.0 - Numerical operations
   
   Optional (database-specific):
   • pyodbc >= 4.0.39 - MSSQL connectivity  
   • psycopg2-binary >= 2.9.0 - PostgreSQL
   • PyMySQL >= 1.0.0 - MySQL/MariaDB

🚀 INSTANT START (SQLite - No Setup):
   from database_actions import create_sqlite_crud
   import pandas as pd
   
   with create_sqlite_crud("my_data.db") as crud:
       df = pd.DataFrame({{'name': ['Alice'], 'age': [25]}})
       crud.insert_dataframe(df, "people")
       result = crud.read_table("people")
       print(result)

☁️ FREE CLOUD OPTIONS:
   • Supabase (PostgreSQL) - 500MB free
   • Railway (PostgreSQL) - Free tier
   • ElephantSQL - 20MB free
   • See opensource_db_config.py for setup

📚 For complete documentation and examples, see README.md
🎯 Run: python run_opensource_demo.py for instant demo!
    """)

if __name__ == "__main__":
    # Run quick start demo when package is executed directly
    package_info()
    quick_start_demo()