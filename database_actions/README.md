# 🗄️ Database Actions - Universal CRUD Framework
## Multi-Database • Pandas Integration • Free Cloud Configurations • No Server Setup Required

Professional database framework supporting MSSQL, SQLite, PostgreSQL, and MySQL with unified CRUD operations, Pandas DataFrame integration, and pre-configured free cloud database options. Perfect for ETL processes, data migration, and database testing.

## ⭐ Key Features

### ✅ Universal Database Support
- **SQLite** - No server setup required, instant local database
- **PostgreSQL** - Open source with advanced features
- **MySQL** - Popular web application database
- **MSSQL** - Enterprise Microsoft SQL Server (via PYODBC)

### ✅ Zero Setup Options
- **In-Memory SQLite** - Instant database testing without files
- **File-Based SQLite** - Persistent local storage
- **Free Cloud Databases** - Pre-configured Supabase, Railway, Aiven connections
- **Docker Integration** - Containerized database environments

### ✅ Pandas Integration
- **DataFrame to Database** - Direct DataFrame insertion
- **Database to DataFrame** - Query results as DataFrames
- **Bulk Operations** - Efficient batch processing
- **Type Mapping** - Automatic Pandas-to-SQL type conversion

### ✅ Enterprise Features
- **Connection Pooling** - Efficient resource management
- **Transaction Support** - ACID compliance with rollback
- **Comprehensive Logging** - Operation tracking and debugging
- **Error Recovery** - Graceful handling of connection issues

## 📁 Project Structure

```
database_actions/
├── README.md                        # 📖 This documentation
├── __init__.py                      # 📦 Package initialization
├── universal_crud_framework.py      # 🎯 Main CRUD framework
├── opensource_db_config.py          # ⚙️ Database configurations
├── run_opensource_demo.py           # 🚀 Instant SQLite demo
├── opensource_crud_examples.py      # 📋 Comprehensive examples
├── quick_start.py                   # 🎯 Interactive setup
└── logs/                            # 📝 Operation logs
    ├── db_operations_YYYYMMDD_HHMMSS.log
    └── error_logs/
```

## 🚀 Quick Start (No Server Required!)

### 1. Instant SQLite Demo
```bash
# Zero setup - starts immediately!
python run_opensource_demo.py
```

### 2. Interactive Configuration
```bash  
# Guided setup for all database types
python quick_start.py
```

### 3. Comprehensive Examples
```bash
# See all CRUD operations in action
python opensource_crud_examples.py
```

## 🎯 Universal CRUD Framework

### Core Class: `UniversalCrudFramework`

```python
from universal_crud_framework import UniversalCrudFramework
import pandas as pd

# SQLite (no server needed)
crud = UniversalCrudFramework('sqlite', database='demo.db')

# PostgreSQL (cloud or local)
crud = UniversalCrudFramework('postgresql', 
    host='db.xxxx.supabase.co', 
    database='postgres',
    username='postgres', 
    password='your-password'
)

# MySQL (cloud or local)  
crud = UniversalCrudFramework('mysql',
    host='containers-us-west-xxx.railway.app',
    port=6543,
    database='railway', 
    username='root',
    password='your-password'
)
```

### Available Methods

| Method | Purpose | Parameters | Returns |
|--------|---------|------------|---------|
| `create_table()` | Create database table | `table_name, columns_dict` | Success status |
| `insert_data()` | Insert records | `table_name, data` | Inserted count |  
| `insert_dataframe()` | Insert DataFrame | `table_name, dataframe` | Inserted count |
| `read_data()` | Query records | `table_name, conditions` | DataFrame |
| `update_data()` | Update records | `table_name, updates, conditions` | Updated count |
| `delete_data()` | Delete records | `table_name, conditions` | Deleted count |
| `execute_query()` | Run custom SQL | `query, params` | Results |

## 🔧 Database Configuration

### 1. SQLite Configuration (Zero Setup)

```python
from opensource_db_config import OpenSourceDBConfig

# In-memory database (temporary)
config = OpenSourceDBConfig.sqlite_memory()

# File-based database (persistent)  
config = OpenSourceDBConfig.sqlite_file('my_database.db')

# Use configuration
crud = config.create_crud_framework()
```

### 2. Free Cloud PostgreSQL (Supabase)

```python
# Free Supabase PostgreSQL
config = OpenSourceDBConfig.supabase_free(
    project_url="https://xxxxxxxxxxxx.supabase.co",
    password="your-secure-password"
)

crud = config.create_crud_framework()
```

### 3. Free Cloud MySQL (Railway)

```python  
# Free Railway MySQL
config = OpenSourceDBConfig.railway_mysql(
    host="containers-us-west-xxx.railway.app",
    port=6543,
    password="your-railway-password"
)

crud = config.create_crud_framework()
```

### 4. Configuration from Environment

```python
import os

# Load from environment variables
config = OpenSourceDBConfig(
    db_type='postgresql',
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', '5432')),
    database=os.getenv('DB_NAME'),
    username=os.getenv('DB_USER'), 
    password=os.getenv('DB_PASSWORD')
)
```

## 📊 Complete CRUD Examples

### 1. Employee Management System

```python
from universal_crud_framework import UniversalCrudFramework
import pandas as pd

# Initialize with SQLite (no server needed)
crud = UniversalCrudFramework('sqlite', database='employees.db')

# Create employees table
columns = {
    'employee_id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT NOT NULL',
    'email': 'TEXT UNIQUE',
    'department': 'TEXT',
    'salary': 'REAL',
    'hire_date': 'DATE',
    'is_active': 'BOOLEAN DEFAULT 1'
}

crud.create_table('employees', columns)

# Insert single employee
employee_data = {
    'name': 'John Doe',
    'email': 'john.doe@company.com', 
    'department': 'Engineering',
    'salary': 75000.00,
    'hire_date': '2024-01-15',
    'is_active': True
}

crud.insert_data('employees', employee_data)

# Insert multiple employees
employees_df = pd.DataFrame([
    {'name': 'Jane Smith', 'email': 'jane@company.com', 'department': 'Marketing', 'salary': 65000},
    {'name': 'Bob Johnson', 'email': 'bob@company.com', 'department': 'Sales', 'salary': 70000},
    {'name': 'Alice Brown', 'email': 'alice@company.com', 'department': 'Engineering', 'salary': 80000}
])

crud.insert_dataframe('employees', employees_df)

# Query operations
all_employees = crud.read_data('employees')
print(f"📊 Total employees: {len(all_employees)}")

# Filter by department
engineers = crud.read_data('employees', {'department': 'Engineering'})
print(f"🔧 Engineers: {len(engineers)}")

# Update salary
crud.update_data('employees', 
    {'salary': 82000}, 
    {'name': 'Alice Brown'}
)

# Delete inactive employees  
crud.delete_data('employees', {'is_active': False})

crud.close()
```

### 2. Large Dataset Processing

```python
def process_large_dataset():
    """Handle large dataset with chunking"""
    
    crud = UniversalCrudFramework('sqlite', database='large_data.db')
    
    # Create table for large dataset
    columns = {
        'id': 'INTEGER PRIMARY KEY', 
        'transaction_id': 'TEXT',
        'amount': 'REAL',
        'category': 'TEXT',
        'timestamp': 'DATETIME'
    }
    
    crud.create_table('transactions', columns)
    
    # Process in chunks (100K rows at a time)
    chunk_size = 100000
    for chunk_num in range(10):  # 1M total rows
        
        # Generate chunk data
        chunk_data = pd.DataFrame({
            'transaction_id': [f'TXN_{chunk_num}_{i}' for i in range(chunk_size)],
            'amount': np.random.uniform(10, 10000, chunk_size),
            'category': np.random.choice(['Food', 'Transport', 'Shopping'], chunk_size),
            'timestamp': pd.date_range('2024-01-01', periods=chunk_size, freq='1min')
        })
        
        # Insert chunk
        inserted = crud.insert_dataframe('transactions', chunk_data)
        print(f"✅ Inserted chunk {chunk_num + 1}: {inserted} rows")
    
    # Analyze data
    summary = crud.execute_query("""
        SELECT category, 
               COUNT(*) as transaction_count,
               AVG(amount) as avg_amount,
               SUM(amount) as total_amount
        FROM transactions 
        GROUP BY category
        ORDER BY total_amount DESC
    """)
    
    print("📊 Transaction Summary:")
    print(summary)
    
    crud.close()
```

## 🌐 Free Cloud Database Setup

### Supabase (PostgreSQL) - Free Tier

**1. Create Account:** [supabase.com](https://supabase.com)  
**2. Create New Project:** Follow setup wizard  
**3. Get Connection Details:**
```python  
config = OpenSourceDBConfig.supabase_free(
    project_url="https://your-project-id.supabase.co",
    password="your-database-password"
)
```

**Free Tier Limits:**
- ✅ 500MB database storage
- ✅ 2GB bandwidth per month
- ✅ Up to 50,000 rows
- ✅ PostgreSQL 15 with full SQL support

### Railway (MySQL) - Free Tier

**1. Create Account:** [railway.app](https://railway.app)  
**2. Deploy MySQL:** Use template or manual setup  
**3. Get Connection Details:**
```python
config = OpenSourceDBConfig.railway_mysql(
    host="containers-us-west-xxx.railway.app", 
    port=6543,  # Check your Railway dashboard
    password="your-generated-password"
)
```

**Free Tier Limits:**
- ✅ $5 monthly credit (enough for development)
- ✅ No storage limit
- ✅ Full MySQL 8.0 features

### Aiven (Multiple Databases) - Free Tier

**Setup:**
```python
# PostgreSQL
config = OpenSourceDBConfig.aiven_postgresql(
    host="your-service-host.aivencloud.com",
    port=25060,
    database="defaultdb", 
    username="avnadmin",
    password="your-aiven-password"
)

# MySQL  
config = OpenSourceDBConfig.aiven_mysql(
    host="your-mysql-host.aivencloud.com",
    port=25061,
    database="defaultdb",
    username="avnadmin", 
    password="your-aiven-password"
)
```

## 📈 Advanced Operations

### Transaction Management
```python
crud = UniversalCrudFramework('postgresql', **config)

try:
    # Begin transaction
    crud.execute_query("BEGIN TRANSACTION")
    
    # Multiple operations
    crud.insert_data('orders', order_data)
    crud.update_data('inventory', {'quantity': 'quantity - 5'}, {'product_id': 123})
    crud.insert_data('order_items', items_data)
    
    # Commit if all successful
    crud.execute_query("COMMIT")
    print("✅ Transaction completed successfully")
    
except Exception as e:
    # Rollback on error
    crud.execute_query("ROLLBACK")
    print(f"❌ Transaction failed: {str(e)}")
```

### Connection Pooling
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Enhanced connection with pooling
config = OpenSourceDBConfig.postgresql_local()
engine = create_engine(
    config.connection_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Validate connections
)

crud = UniversalCrudFramework(engine=engine)
```

### Complex Queries  
```python
# Join operations
complex_query = """
SELECT e.name, e.department, d.budget, e.salary,
       (e.salary / d.budget * 100) as salary_percentage
FROM employees e
JOIN departments d ON e.department = d.name  
WHERE e.is_active = 1 
  AND e.salary > d.avg_salary
ORDER BY salary_percentage DESC
LIMIT 10
"""

top_earners = crud.execute_query(complex_query)
print("💰 Top earners by department budget percentage:")
print(top_earners)
```

## 🚨 Error Handling & Recovery

### Connection Retry Logic
```python
def robust_database_operation():
    """Database operation with retry logic"""
    
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            crud = UniversalCrudFramework('postgresql', **config)
            result = crud.read_data('users', {'active': True})
            crud.close()
            return result
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
            else:
                print("💥 All retry attempts exhausted")
                raise e
```

### Database Health Check
```python
def check_database_health(config: OpenSourceDBConfig) -> dict:
    """Check database connection and performance"""
    
    health_status = {
        'connection': False,
        'response_time': None,
        'table_count': None,
        'error': None
    }
    
    try:
        start_time = time.time()
        crud = UniversalCrudFramework(config.db_type, **config.connection_params)
        
        # Test basic operations
        tables = crud.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        
        health_status.update({
            'connection': True,
            'response_time': time.time() - start_time,
            'table_count': len(tables)
        })
        
        crud.close()
        
    except Exception as e:
        health_status['error'] = str(e)
    
    return health_status
```

## 📊 Performance Monitoring

### Operation Timing
```python
import time
from contextlib import contextmanager

@contextmanager
def timed_operation(operation_name: str):
    """Context manager for timing database operations"""
    start_time = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        print(f"⏱️ {operation_name}: {elapsed:.3f} seconds")

# Usage example
with timed_operation("Large DataFrame Insert"):
    crud.insert_dataframe('bulk_data', large_dataframe)
    
with timed_operation("Complex Query"):
    results = crud.execute_query(complex_analytics_query)
```

### Memory Usage Tracking
```python
import psutil
import os

def monitor_memory_usage():
    """Monitor memory usage during database operations"""
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"🧠 Initial memory: {initial_memory:.1f} MB")
    
    # Perform database operations
    crud = UniversalCrudFramework('sqlite', database='memory_test.db')
    
    # Large operation
    big_df = pd.DataFrame(np.random.randn(100000, 50))
    crud.insert_dataframe('test_table', big_df)
    
    peak_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = peak_memory - initial_memory
    
    print(f"🧠 Peak memory: {peak_memory:.1f} MB (+{memory_increase:.1f} MB)")
    
    crud.close()
```

## 🔧 Troubleshooting

### Common Issues

**1. SQLite File Permissions**
```python
import os
import stat

# Ensure database file is writable
db_file = 'my_database.db'
if os.path.exists(db_file):
    os.chmod(db_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)
```

**2. PostgreSQL Connection Issues**
```python
# Check connection with detailed error info
try:
    crud = UniversalCrudFramework('postgresql', 
        host='localhost', port=5432,
        database='testdb', username='user', password='pass')
except Exception as e:
    if 'could not connect' in str(e).lower():
        print("🔍 Check if PostgreSQL server is running")
        print("🔍 Verify host, port, and credentials")
        print("🔍 Check firewall settings") 
    elif 'authentication failed' in str(e).lower():
        print("🔍 Verify username and password")
        print("🔍 Check database user permissions")
```

**3. Pandas DataFrame Type Issues**
```python
# Handle mixed data types in DataFrame
def clean_dataframe_for_insert(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame for database insertion"""
    
    df_clean = df.copy()
    
    # Convert object columns with mixed types
    for col in df_clean.select_dtypes(include=['object']).columns:
        df_clean[col] = df_clean[col].astype(str)
    
    # Handle NaN values
    df_clean = df_clean.fillna('')
    
    # Ensure datetime columns are properly formatted
    for col in df_clean.select_dtypes(include=['datetime64']).columns:
        df_clean[col] = df_clean[col].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    return df_clean
```

## 🏢 Enterprise Integration

### Environment Configuration
```bash
# .env file
DB_TYPE=postgresql
DB_HOST=prod-db.company.com
DB_PORT=5432
DB_NAME=production
DB_USER=app_user
DB_PASSWORD=secure_password
DB_SSL_MODE=require
```

```python
# Load environment configuration
from dotenv import load_dotenv
import os

load_dotenv()

config = OpenSourceDBConfig(
    db_type=os.getenv('DB_TYPE'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME'),
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
```

### CI/CD Pipeline Integration
```yaml
# .github/workflows/database-tests.yml
name: Database Integration Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test_password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run database tests  
        run: python opensource_crud_examples.py
        env:
          DB_HOST: localhost
          DB_PASSWORD: test_password
```

## 📚 Additional Resources

### Related Documentation
- 🚀 [API Testing](../API_Testing/README.md) - API endpoint testing for database APIs
- 📊 [Pandas Analysis](../pandas_analysis/README.md) - Advanced data analysis with DataFrames  
- 🕷️ [Selenium Testing](../selenium%20Testing/README.md) - Web application database testing

### External References
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pandas DataFrame API](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) 
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**🗄️ Built for enterprise data management and migration**  

*Universal • Reliable • Production-Ready* ✨