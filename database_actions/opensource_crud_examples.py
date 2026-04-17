"""
Open Source Database CRUD Examples & Testing
==========================================
Author: System Assistant
Date: April 13, 2026

Complete examples for open source database CRUD operations:
- SQLite: No server needed, perfect for immediate testing
- PostgreSQL: Free cloud options
- MySQL: Open source alternative examples
- All examples work without localhost setup
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from universal_crud_framework import UniversalCrudFramework, create_sqlite_crud, create_memory_crud
    from opensource_db_config import (
        OpenSourceDBConfig, 
        setup_sqlite_database,
        create_sample_sqlite_database,
        print_free_database_options,
        SQLITE_CONFIGS,
        POSTGRESQL_CLOUD_CONFIGS,
        get_sqlalchemy_url
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all framework files are in the same directory")
    sys.exit(1)

def create_sample_data(num_records: int = 50) -> pd.DataFrame:
    """
    Create sample employee data for testing.
    
    Args:
        num_records (int): Number of records to generate
        
    Returns:
        pd.DataFrame: Sample employee data
    """
    np.random.seed(42)  # For reproducible data
    
    departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations']
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emma', 'Chris', 'Lisa', 'Tom', 'Anna']
    last_names = ['Smith', 'Johnson', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas']
    
    data = {
        'employee_id': range(1, num_records + 1),
        'first_name': np.random.choice(first_names, num_records),
        'last_name': np.random.choice(last_names, num_records), 
        'email': [f"employee{i}@company.com" for i in range(1, num_records + 1)],
        'department': np.random.choice(departments, num_records),
        'salary': np.random.normal(75000, 20000, num_records).astype(int),
        'hire_date': pd.date_range(start='2020-01-01', end='2024-12-31', periods=num_records),
        'is_active': np.random.choice([True, False], num_records, p=[0.85, 0.15]),
        'performance_rating': np.random.choice([1, 2, 3, 4, 5], num_records, p=[0.05, 0.15, 0.4, 0.3, 0.1])
    }
    
    df = pd.DataFrame(data)
    
    # Ensure salary is positive and realistic
    df['salary'] = df['salary'].abs().clip(30000, 200000)
    
    return df

def demo_sqlite_operations():
    """
    Demonstrate SQLite operations - no server setup required!
    """
    
    print("🗄️ SQLITE DATABASE DEMO (NO SERVER NEEDED)")
    print("=" * 50)
    
    # SQLite requires no server setup - it's just a file!
    db_file = "demo_employees.db"
    
    try:
        with create_sqlite_crud(db_file) as crud:
            
            # Test connection
            print("🔌 Testing SQLite connection...")
            if crud.test_connection():
                print("✅ SQLite connection successful!")
            else:
                print("❌ SQLite connection failed")
                return False
                
            print(f"📁 Database file: {os.path.abspath(db_file)}")
            
            # ==========================================
            # CREATE OPERATIONS
            # ==========================================
            
            print("\n📥 CREATE OPERATIONS")
            print("-" * 30)
            
            # Generate sample data
            sample_df = create_sample_data(30)
            print(f"Generated {len(sample_df)} employee records")
            
            # Insert DataFrame using pandas to_sql
            print("🔄 Inserting data using pandas to_sql...")
            success = crud.insert_dataframe(
                df=sample_df,
                table_name="employees",
                if_exists="replace"  # Create new table
            )
            
            if success:
                print("✅ Employee data inserted successfully")
            
            # Insert additional records
            print("\n🔄 Adding new employees...")
            new_employees = [
                {
                    'employee_id': 100,
                    'first_name': 'Alice',
                    'last_name': 'Cooper',
                    'email': 'alice.cooper@company.com',
                    'department': 'IT',
                    'salary': 90000,
                    'hire_date': '2024-04-01',
                    'is_active': True,
                    'performance_rating': 4
                },
                {
                    'employee_id': 101,
                    'first_name': 'Bob',
                    'last_name': 'Dylan',
                    'email': 'bob.dylan@company.com', 
                    'department': 'Marketing',
                    'salary': 85000,
                    'hire_date': '2024-04-01',
                    'is_active': True,
                    'performance_rating': 5
                }
            ]
            
            crud.insert_records("employees", new_employees)
            print("✅ New employees added")
            
            # ==========================================
            # READ OPERATIONS 
            # ==========================================
            
            print("\n📤 READ OPERATIONS")
            print("-" * 30)
            
            # Read entire table with limit
            print("📖 Reading employee data...")
            all_employees = crud.read_table("employees", limit=10)
            print(f"Retrieved {len(all_employees)} records (showing first 10)")
            print("\nSample data:")
            print(all_employees[['employee_id', 'first_name', 'last_name', 'department', 'salary']].head())
            
            # Read with conditions
            print("\n📖 Finding high-performing IT employees...")
            it_stars = crud.read_with_conditions(
                table_name="employees",
                conditions={"department": "IT", "performance_rating": 4},
                columns=["employee_id", "first_name", "last_name", "salary", "performance_rating"]
            )
            print(f"Found {len(it_stars)} high-performing IT employees")
            if not it_stars.empty:
                print(it_stars)
            
            # Custom query
            print("\n📖 Department salary analysis...")
            salary_analysis = crud.read_query("""
                SELECT 
                    department,
                    COUNT(*) as employee_count,
                    ROUND(AVG(salary), 2) as avg_salary,
                    MIN(salary) as min_salary,
                    MAX(salary) as max_salary
                FROM employees 
                WHERE is_active = 1
                GROUP BY department
                ORDER BY avg_salary DESC
            """)
            print("📊 Department Salary Analysis:")
            print(salary_analysis)
            
            # ==========================================
            # UPDATE OPERATIONS
            # ==========================================
            
            print("\n🔄 UPDATE OPERATIONS")
            print("-" * 30)
            
            # Give raises to high performers
            print("💰 Giving raises to top performers...")
            rows_updated = crud.update_records(
                table_name="employees",
                set_values={"salary": 95000},
                conditions={"performance_rating": 5}
            )
            print(f"✅ Updated salaries for {rows_updated} top performers")
            
            # Update department for specific employee
            print("\n🔄 Promoting Alice Cooper to Management...")
            promotion_update = crud.update_records(
                table_name="employees", 
                set_values={"department": "Management", "salary": 110000},
                conditions={"first_name": "Alice", "last_name": "Cooper"}
            )
            print(f"✅ Updated {promotion_update} employee record")
            
            # ==========================================
            # DELETE OPERATIONS
            # ==========================================
            
            print("\n🗑️ DELETE OPERATIONS")
            print("-" * 30)
            
            # Remove inactive employees
            print("🧹 Removing inactive employees...")
            deleted_count = crud.delete_records(
                table_name="employees",
                conditions={"is_active": False}
            )
            print(f"✅ Removed {deleted_count} inactive employees")
            
            # ==========================================
            # UTILITY OPERATIONS
            # ==========================================
            
            print("\n🔧 UTILITY OPERATIONS")
            print("-" * 30)
            
            # Get table structure
            print("📋 Table structure:")
            table_info = crud.get_table_info("employees")
            print(table_info[['column_name', 'data_type', 'nullable']])
            
            # Get row counts
            total_employees = crud.get_row_count("employees")
            active_employees = crud.get_row_count("employees", conditions={"is_active": True})
            
            print(f"\n📊 Database Statistics:")
            print(f"   Total employees: {total_employees}")
            print(f"   Active employees: {active_employees}")
            
            # List all tables
            tables = crud.list_tables()
            print(f"   Database tables: {tables}")
            
            # ==========================================
            # CSV OPERATIONS
            # ==========================================
            
            print("\n📁 CSV OPERATIONS")
            print("-" * 30)
            
            # Export to CSV
            print("📤 Exporting data to CSV...")
            export_data = crud.read_query("""
                SELECT employee_id, first_name, last_name, email, department, salary
                FROM employees
                WHERE is_active = 1
                ORDER BY department, last_name
            """)
            
            csv_file = "active_employees_export.csv"
            export_data.to_csv(csv_file, index=False)
            print(f"✅ Exported {len(export_data)} active employees to {csv_file}")
            
            # Import additional data from CSV
            print("\n📥 Creating and importing additional CSV data...")
            
            # Create additional sample data
            additional_data = pd.DataFrame({
                'employee_id': [200, 201, 202],
                'first_name': ['Carol', 'Dave', 'Eve'],
                'last_name': ['White', 'Black', 'Green'],
                'email': ['carol.white@company.com', 'dave.black@company.com', 'eve.green@company.com'],
                'department': ['HR', 'Finance', 'Operations'],
                'salary': [70000, 80000, 75000],
                'hire_date': ['2024-05-01', '2024-05-01', '2024-05-01'],
                'is_active': [True, True, True],
                'performance_rating': [3, 4, 3]
            })
            
            import_csv = "new_hires.csv"
            additional_data.to_csv(import_csv, index=False)
            
            # Import from CSV
            print(f"📥 Importing new hires from {import_csv}...")
            crud.bulk_insert_csv(import_csv, "employees")
            print("✅ New hires imported successfully")
            
            # Final statistics
            final_count = crud.get_row_count("employees")
            print(f"\n📊 Final employee count: {final_count}")
            
            # Clean up CSV files
            for csv in [csv_file, import_csv]:
                if os.path.exists(csv):
                    os.remove(csv)
                    print(f"🧹 Cleaned up {csv}")
            
            print(f"\n🎉 SQLite demo completed successfully!")
            print(f"💡 Database file '{db_file}' contains all your data")
            print(f"   You can open it with any SQLite browser or keep using the framework")
            
            return True
            
    except Exception as e:
        print(f"❌ SQLite demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def demo_memory_database():
    """
    Demonstrate in-memory SQLite database - ultra-fast testing!
    """
    
    print("\n💾 IN-MEMORY DATABASE DEMO")
    print("=" * 40)
    
    try:
        with create_memory_crud() as crud:
            
            print("🚀 Using in-memory SQLite database (ultra-fast!)")
            
            # Test connection
            if not crud.test_connection():
                print("❌ Memory database connection failed")
                return False
            
            print("✅ In-memory database ready")
            
            # Quick operations demo
            print("\n⚡ Quick operations on memory database...")
            
            # Create sample data
            quick_data = pd.DataFrame({
                'id': [1, 2, 3, 4, 5],
                'name': ['Test1', 'Test2', 'Test3', 'Test4', 'Test5'],
                'value': [10.5, 20.7, 30.2, 40.8, 50.1],
                'category': ['A', 'B', 'A', 'C', 'B']
            })
            
            # Insert data
            crud.insert_dataframe(quick_data, "test_data", if_exists="replace")
            print(f"📥 Inserted {len(quick_data)} test records")
            
            # Query data  
            results = crud.read_query("""
                SELECT category, COUNT(*) as count, ROUND(AVG(value), 2) as avg_value
                FROM test_data 
                GROUP BY category
                ORDER BY avg_value DESC
            """)
            
            print("📊 Category analysis:")
            print(results)
            
            # Update data
            updated = crud.update_records(
                "test_data", 
                {"value": 100.0}, 
                {"category": "A"}
            )
            print(f"🔄 Updated {updated} category A records")
            
            # Final count
            final_count = crud.get_row_count("test_data")
            print(f"📊 Final record count: {final_count}")
            
            print("✅ In-memory database demo completed!")
            print("💡 Data exists only in memory - perfect for testing and temporary operations")
            
            return True
            
    except Exception as e:
        print(f"❌ Memory database demo failed: {str(e)}")
        return False

def demo_advanced_sqlite_features():
    """
    Demonstrate advanced SQLite features and analytics.
    """
    
    print("\n🔬 ADVANCED SQLITE FEATURES DEMO") 
    print("=" * 40)
    
    db_file = "advanced_demo.db"
    
    try:
        with create_sqlite_crud(db_file) as crud:
            
            print("🏗️ Creating normalized database structure...")
            
            # Create departments table
            departments_df = pd.DataFrame({
                'dept_id': [1, 2, 3, 4, 5],
                'dept_name': ['IT', 'HR', 'Finance', 'Marketing', 'Sales'],
                'budget': [1000000, 500000, 800000, 600000, 900000],
                'location': ['Building A', 'Building B', 'Building A', 'Building C', 'Building B']
            })
            
            crud.insert_dataframe(departments_df, "departments", if_exists="replace")
            print("✅ Departments table created")
            
            # Create projects table
            projects_df = pd.DataFrame({
                'project_id': range(1, 11),
                'project_name': [f'Project {i}' for i in range(1, 11)],
                'dept_id': np.random.choice([1, 2, 3, 4, 5], 10),
                'budget': np.random.randint(50000, 500000, 10),
                'start_date': pd.date_range('2024-01-01', periods=10, freq='30D'),
                'status': np.random.choice(['Active', 'Completed', 'On Hold'], 10)
            })
            
            crud.insert_dataframe(projects_df, "projects", if_exists="replace")
            print("✅ Projects table created")
            
            # Create employees with department references
            employees_df = create_sample_data(40)
            employees_df['dept_id'] = np.random.choice([1, 2, 3, 4, 5], len(employees_df))
            
            crud.insert_dataframe(employees_df, "employees", if_exists="replace")
            print("✅ Employees table created with department references")
            
            # Advanced analytics queries
            print("\n📊 Advanced Analytics...")
            
            # Cross-table analysis
            dept_analysis = crud.read_query("""
                SELECT 
                    d.dept_name,
                    d.budget as dept_budget,
                    COUNT(e.employee_id) as employee_count,
                    ROUND(AVG(e.salary), 2) as avg_salary,
                    COUNT(p.project_id) as project_count,
                    ROUND(AVG(p.budget), 2) as avg_project_budget
                FROM departments d
                LEFT JOIN employees e ON d.dept_id = e.dept_id
                LEFT JOIN projects p ON d.dept_id = p.dept_id
                WHERE e.is_active = 1
                GROUP BY d.dept_id, d.dept_name, d.budget
                ORDER BY employee_count DESC
            """)
            
            print("🏢 Department Analysis:")
            print(dept_analysis)
            
            # Performance vs budget analysis
            performance_analysis = crud.read_query("""
                SELECT 
                    e.performance_rating,
                    COUNT(*) as employee_count,
                    ROUND(AVG(e.salary), 2) as avg_salary,
                    d.dept_name,
                    d.budget
                FROM employees e
                JOIN departments d ON e.dept_id = d.dept_id
                WHERE e.is_active = 1
                GROUP BY e.performance_rating, d.dept_name, d.budget
                ORDER BY e.performance_rating DESC, avg_salary DESC
            """)
            
            print("\n⭐ Performance vs Salary Analysis:")
            print(performance_analysis.head(10))
            
            # Project status summary
            project_summary = crud.read_query("""
                SELECT 
                    p.status,
                    COUNT(*) as project_count,
                    SUM(p.budget) as total_budget,
                    ROUND(AVG(p.budget), 2) as avg_budget,
                    GROUP_CONCAT(DISTINCT d.dept_name) as departments
                FROM projects p
                JOIN departments d ON p.dept_id = d.dept_id
                GROUP BY p.status
                ORDER BY total_budget DESC
            """)
            
            print("\n🎯 Project Status Summary:")
            print(project_summary)
            
            # Create summary export
            print("\n📁 Creating comprehensive data export...")
            
            full_export = crud.read_query("""
                SELECT 
                    e.employee_id,
                    e.first_name || ' ' || e.last_name as full_name,
                    e.email,
                    d.dept_name as department,
                    e.salary,
                    e.performance_rating,
                    e.hire_date,
                    d.budget as dept_budget,
                    COUNT(p.project_id) as assigned_projects
                FROM employees e
                JOIN departments d ON e.dept_id = d.dept_id
                LEFT JOIN projects p ON d.dept_id = p.dept_id
                WHERE e.is_active = 1
                GROUP BY e.employee_id, e.first_name, e.last_name, e.email, 
                         d.dept_name, e.salary, e.performance_rating, e.hire_date, d.budget
                ORDER BY d.dept_name, e.performance_rating DESC
            """)
            
            export_file = "comprehensive_employee_report.csv"
            full_export.to_csv(export_file, index=False)
            print(f"✅ Comprehensive report exported to {export_file}")
            print(f"   Contains {len(full_export)} employee records with department and project data")
            
            # Clean up
            if os.path.exists(export_file):
                os.remove(export_file)
                print(f"🧹 Cleaned up {export_file}")
            
            print(f"\n🎉 Advanced SQLite demo completed!")
            print(f"💾 Advanced database saved as: {os.path.abspath(db_file)}")
            
            return True
            
    except Exception as e:
        print(f"❌ Advanced SQLite demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def show_cloud_database_setup():
    """
    Show how to set up free cloud databases.
    """
    
    print("\n☁️ FREE CLOUD DATABASE SETUP GUIDE")
    print("=" * 45)
    
    print_free_database_options()
    
    print("\n🔧 EXAMPLE CONFIGURATIONS")
    print("-" * 30)
    
    # Show example configurations (with placeholder values)
    print("\n1️⃣ Supabase PostgreSQL Example:")
    print("""
config = OpenSourceDBConfig(
    db_type="postgresql",
    host="db.your-project.supabase.co",
    port=5432,
    database="postgres", 
    username="postgres",
    password="your-super-secret-password",
    connection_params={"sslmode": "require"}
)

with UniversalCrudFramework(config) as crud:
    df = crud.read_table("your_table")
    """)
    
    print("\n2️⃣ Railway PostgreSQL Example:")
    print("""
config = OpenSourceDBConfig(
    db_type="postgresql",
    host="containers-us-west-1.railway.app", 
    port=5432,
    database="railway",
    username="postgres",
    password="your-railway-password"
)

with UniversalCrudFramework(config) as crud:
    crud.insert_dataframe(df, "my_table")
    """)
    
    print("\n💡 QUICK START RECOMMENDATIONS:")
    print("1. Start with SQLite (no setup required)")
    print("2. Try in-memory database for testing")
    print("3. Move to cloud PostgreSQL for production")
    print("4. Check the comprehensive examples above")

def main():
    """
    Run comprehensive open source database demo.
    """
    
    print("🌟 OPEN SOURCE DATABASE CRUD FRAMEWORK")
    print("=====================================")
    print("No localhost setup required! 🎉")
    print()
    
    # Show available options first
    show_cloud_database_setup()
    
    print("\n" + "="*50)
    print("🚀 RUNNING LIVE DEMOS...")
    
    # Run SQLite demo (always works)
    success1 = demo_sqlite_operations()
    
    if success1:
        # Run memory demo
        success2 = demo_memory_database()
        
        if success2:
            # Run advanced demo
            success3 = demo_advanced_sqlite_features()
            
            if success3:
                print("\n" + "="*50)
                print("🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
                print("\n📚 What you learned:")
                print("✅ SQLite file-based database (no server needed)")
                print("✅ In-memory database for ultra-fast testing")
                print("✅ Complete CRUD operations with pandas")
                print("✅ Advanced analytics and multi-table operations")
                print("✅ CSV import/export capabilities")
                print("✅ Professional logging and error handling")
                
                print("\n🎯 Next steps:")
                print("• Use SQLite for immediate development")
                print("• Try free cloud PostgreSQL for production")
                print("• Explore the universal framework for other databases")
                print("• Check the database files created in current directory")
                
                # List created files
                demo_files = [f for f in os.listdir('.') if f.endswith('.db')]
                if demo_files:
                    print(f"\n📁 Demo database files created:")
                    for file in demo_files:
                        size = os.path.getsize(file) / 1024  # KB
                        print(f"   • {file} ({size:.1f} KB)")
                
                return True
    
    print("\n❌ Some demos failed. Check the error messages above.")
    return False

