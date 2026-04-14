"""
Open Source Database Configurations
==================================
Author: System Assistant
Date: April 13, 2026

Support for popular open source databases that don't require localhost setup:
- SQLite: File-based database, no server needed
- PostgreSQL: Free cloud instances and Docker options
- MySQL/MariaDB: Open source alternatives
- Cloud-hosted free database services
"""

import os
import sqlite3
from typing import Dict, Optional, Any
from dataclasses import dataclass
import urllib.parse

@dataclass 
class OpenSourceDBConfig:
    """Configuration for open source databases."""
    
    db_type: str  # 'sqlite', 'postgresql', 'mysql'
    database: str
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    connection_params: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate configuration."""
        if self.db_type not in ['sqlite', 'postgresql', 'mysql']:
            raise ValueError("Supported db_types: sqlite, postgresql, mysql")
        
        if self.db_type == 'sqlite':
            # For SQLite, database is the file path
            pass
        else:
            # For server databases, host is required
            if not self.host:
                raise ValueError(f"Host is required for {self.db_type}")

# ==========================================
# SQLITE CONFIGURATIONS (NO SERVER NEEDED)
# ==========================================

SQLITE_CONFIGS = {
    "local_file": OpenSourceDBConfig(
        db_type="sqlite",
        database="test_database.db"  # Will be created in current directory
    ),
    
    "memory_db": OpenSourceDBConfig(
        db_type="sqlite", 
        database=":memory:"  # In-memory database, perfect for testing
    ),
    
    "temp_file": OpenSourceDBConfig(
        db_type="sqlite",
        database="temp_test.db"
    )
}

# ==========================================
# FREE CLOUD POSTGRESQL SERVICES
# ==========================================

POSTGRESQL_CLOUD_CONFIGS = {
    "supabase_free": OpenSourceDBConfig(
        db_type="postgresql",
        host="db.your-project.supabase.co",
        port=5432,
        database="postgres",
        username="postgres",
        password="your-password",
        connection_params={
            "sslmode": "require"
        }
    ),
    
    "railway_free": OpenSourceDBConfig(
        db_type="postgresql", 
        host="containers-us-west-1.railway.app",
        port=5432,
        database="railway",
        username="postgres",
        password="your-password"
    ),
    
    "aiven_free": OpenSourceDBConfig(
        db_type="postgresql",
        host="your-service.aivencloud.com",
        port=5432,
        database="defaultdb",
        username="avnadmin",
        password="your-password",
        connection_params={
            "sslmode": "require"
        }
    ),
    
    "elephantsql_free": OpenSourceDBConfig(
        db_type="postgresql",
        host="bubble.db.elephantsql.com",
        port=5432, 
        database="your-database-name",
        username="your-username",
        password="your-password"
    )
}

# ==========================================
# MYSQL/MARIADB CONFIGURATIONS  
# ==========================================

MYSQL_CONFIGS = {
    "planetscale_free": OpenSourceDBConfig(
        db_type="mysql",
        host="gateway01.ap-southeast-1.prod.aws.planetscale.sh", 
        port=3306,
        database="your-database",
        username="your-username",
        password="your-password",
        connection_params={
            "ssl_disabled": False
        }
    ),
    
    "freemysqlhosting": OpenSourceDBConfig(
        db_type="mysql",
        host="sql12.freemysqlhosting.net",
        port=3306,
        database="your-database",
        username="your-username", 
        password="your-password"
    )
}

# ==========================================
# CONNECTION STRING BUILDERS
# ==========================================

def build_sqlite_url(config: OpenSourceDBConfig) -> str:
    """Build SQLite connection URL for SQLAlchemy."""
    database_path = config.database
    
    if database_path == ":memory:":
        return "sqlite:///:memory:"
    else:
        # Convert to absolute path
        if not os.path.isabs(database_path):
            database_path = os.path.abspath(database_path)
        return f"sqlite:///{database_path}"

def build_postgresql_url(config: OpenSourceDBConfig) -> str:
    """Build PostgreSQL connection URL for SQLAlchemy."""
    url = f"postgresql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
    
    if config.connection_params:
        params = urllib.parse.urlencode(config.connection_params)
        url += f"?{params}"
    
    return url

def build_mysql_url(config: OpenSourceDBConfig) -> str:
    """Build MySQL connection URL for SQLAlchemy."""
    url = f"mysql+pymysql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
    
    if config.connection_params:
        params = urllib.parse.urlencode(config.connection_params)
        url += f"?{params}"
    
    return url

def get_sqlalchemy_url(config: OpenSourceDBConfig) -> str:
    """Get SQLAlchemy URL for any supported database type."""
    if config.db_type == "sqlite":
        return build_sqlite_url(config)
    elif config.db_type == "postgresql":
        return build_postgresql_url(config)
    elif config.db_type == "mysql":
        return build_mysql_url(config)
    else:
        raise ValueError(f"Unsupported database type: {config.db_type}")

# ==========================================
# QUICK SETUP FUNCTIONS
# ==========================================

def setup_sqlite_database(db_file: str = "test_database.db") -> OpenSourceDBConfig:
    """
    Set up SQLite database (easiest option - no server needed).
    
    Args:
        db_file: SQLite database file path
        
    Returns:
        OpenSourceDBConfig: SQLite configuration
    """
    return OpenSourceDBConfig(
        db_type="sqlite",
        database=db_file
    )

def setup_memory_database() -> OpenSourceDBConfig:
    """
    Set up in-memory SQLite database (perfect for testing).
    
    Returns:
        OpenSourceDBConfig: In-memory SQLite configuration
    """
    return OpenSourceDBConfig(
        db_type="sqlite", 
        database=":memory:"
    )

def create_sample_sqlite_database(db_file: str = "sample_employees.db") -> str:
    """
    Create a sample SQLite database with test data.
    
    Args:
        db_file: Database file name
        
    Returns:
        str: Path to created database file
    """
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create connection
    conn = sqlite3.connect(db_file)
    
    try:
        # Create employees table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            salary REAL,
            hire_date TEXT,
            is_active BOOLEAN DEFAULT 1,
            manager_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        conn.execute(create_table_sql)
        
        # Generate sample data
        np.random.seed(42)
        n_employees = 50
        
        employees_data = []
        departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales']
        
        for i in range(1, n_employees + 1):
            employee = {
                'employee_id': i,
                'first_name': f'FirstName{i}',
                'last_name': f'LastName{i}',
                'email': f'employee{i}@company.com',
                'department': np.random.choice(departments),
                'salary': round(np.random.normal(75000, 15000), 2),
                'hire_date': (datetime.now() - timedelta(days=np.random.randint(30, 1095))).strftime('%Y-%m-%d'),
                'is_active': np.random.choice([True, False], p=[0.9, 0.1]),
                'manager_id': np.random.randint(1, 11) if i > 10 else None
            }
            employees_data.append(employee)
        
        # Insert sample data using pandas
        df = pd.DataFrame(employees_data)
        df.to_sql('employees', conn, if_exists='replace', index=False)
        
        # Create departments table
        departments_data = pd.DataFrame({
            'dept_id': range(1, len(departments) + 1),
            'dept_name': departments,
            'budget': [500000, 300000, 800000, 400000, 600000]
        })
        
        departments_data.to_sql('departments', conn, if_exists='replace', index=False)
        
        print(f"✅ Sample SQLite database created: {db_file}")
        print(f"   📊 {len(df)} employees in {len(departments)} departments")
        
        return os.path.abspath(db_file)
        
    finally:
        conn.close()

# ==========================================
# FREE CLOUD DATABASE SETUP GUIDES
# ==========================================

def print_free_database_options():
    """Print information about free cloud database options."""
    
    print("🌐 FREE CLOUD DATABASE OPTIONS")
    print("=" * 40)
    
    print("\n1️⃣ SQLite (Recommended for Getting Started)")
    print("   • No server setup required")
    print("   • File-based database")
    print("   • Perfect for development and testing")
    print("   • Use: setup_sqlite_database('my_db.db')")
    
    print("\n2️⃣ Supabase (PostgreSQL)")
    print("   • Free tier: 500MB storage, 2 projects")
    print("   • Real-time features, built-in auth")
    print("   • Sign up: https://supabase.com")
    print("   • Get connection details from dashboard")
    
    print("\n3️⃣ Railway (PostgreSQL)")  
    print("   • Free tier with usage limits")
    print("   • Easy deployment, good for development")
    print("   • Sign up: https://railway.app")
    print("   • Deploy PostgreSQL database with one click")
    
    print("\n4️⃣ Aiven (PostgreSQL)")
    print("   • 1-month free trial")
    print("   • Managed cloud databases")
    print("   • Sign up: https://aiven.io")
    print("   • Choose PostgreSQL service")
    
    print("\n5️⃣ ElephantSQL (PostgreSQL)")
    print("   • Free tier: 20MB storage")
    print("   • Simple setup, good for small projects")
    print("   • Sign up: https://elephantsql.com")
    print("   • Create free 'Tiny Turtle' instance")
    
    print("\n6️⃣ PlanetScale (MySQL)")
    print("   • Free tier: 1 database, 1GB storage")
    print("   • Serverless MySQL platform")
    print("   • Sign up: https://planetscale.com")
    print("   • Create free database")

def get_required_packages(db_type: str) -> list:
    """Get required Python packages for database type."""
    
    base_packages = ["sqlalchemy>=2.0.0", "pandas>=2.1.0"]
    
    if db_type == "sqlite": 
        # SQLite support is built into Python
        return base_packages
        
    elif db_type == "postgresql":
        return base_packages + ["psycopg2-binary>=2.9.0"]
        
    elif db_type == "mysql":
        return base_packages + ["PyMySQL>=1.0.0"]
        
    else:
        return base_packages

def create_requirements_for_db(db_type: str, filename: str = None) -> str:
    """Create requirements.txt file for specific database type."""
    
    if filename is None:
        filename = f"requirements_{db_type}.txt"
    
    packages = get_required_packages(db_type)
    
    content = f"""# Requirements for {db_type.upper()} database operations
# Install with: pip install -r {filename}

# Core packages
{chr(10).join(packages)}

# Optional packages for enhanced functionality
numpy>=1.24.0
python-dotenv>=1.0.0

# For {db_type} specific features:
"""
    
    if db_type == "postgresql":
        content += """
# PostgreSQL specific
# psycopg2-binary>=2.9.0  # Already included above
"""
    elif db_type == "mysql":
        content += """
# MySQL specific  
# PyMySQL>=1.0.0  # Already included above
cryptography>=3.4.8  # For MySQL SSL connections
"""
    elif db_type == "sqlite":
        content += """
# SQLite specific
# No additional packages needed - SQLite is built into Python
"""
    
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"✅ Requirements file created: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Failed to create requirements file: {e}")
        return ""

# ==========================================
# EXAMPLE CONFIGURATIONS
# ==========================================

if __name__ == "__main__":
    # Print available options
    print_free_database_options()
    
    # Create sample SQLite database
    print(f"\n📁 Creating sample SQLite database...")
    db_path = create_sample_sqlite_database("sample_employees.db")
    
    # Show configuration examples
    print(f"\n📋 Example configurations:")
    
    # SQLite example
    sqlite_config = setup_sqlite_database("sample_employees.db")
    sqlite_url = get_sqlalchemy_url(sqlite_config)
    print(f"SQLite URL: {sqlite_url}")
    
    # PostgreSQL example (template)
    pg_config = POSTGRESQL_CLOUD_CONFIGS["supabase_free"]
    pg_url = get_sqlalchemy_url(pg_config)
    print(f"PostgreSQL URL: {pg_url}")
    
    # Create requirements files
    print(f"\n📦 Creating requirements files...")
    create_requirements_for_db("sqlite")
    create_requirements_for_db("postgresql") 
    create_requirements_for_db("mysql")