"""
Open Source Database Quick Start
===============================
Author: System Assistant  
Date: April 13, 2026

🚀 INSTANT DATABASE TESTING - NO SERVER SETUP REQUIRED!

This script demonstrates database operations using SQLite, which requires
no server installation, no localhost setup, and no configuration.
Perfect for immediate testing and development!
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_requirements():
    """Check if required packages are installed."""
    print("📦 Checking package requirements...")
    
    required = {
        'pandas': None,
        'numpy': None, 
        'sqlalchemy': None
    }
    
    missing = []
    
    for package in required:
        try:
            if package == 'pandas':
                import pandas as pd
                required[package] = pd.__version__
            elif package == 'numpy':
                import numpy as np
                required[package] = np.__version__
            elif package == 'sqlalchemy':
                import sqlalchemy as sa
                required[package] = sa.__version__
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("\n📥 Install with:")
        print("pip install pandas numpy sqlalchemy")
        return False
    else:
        print("✅ All required packages available:")
        for pkg, version in required.items():
            print(f"   • {pkg}: {version}")
        return True

def instant_sqlite_demo():
    """
    Instant SQLite database demo - works immediately!
    No server, no setup, no configuration needed.
    """
    
    print("\n🗄️ INSTANT SQLITE DATABASE DEMO")
    print("=" * 40)
    print("✨ SQLite = No server required, just works!")
    
    try:
        # Import framework components
        from universal_crud_framework import create_sqlite_crud
        import pandas as pd
        import numpy as np
        
        # Create SQLite database (just a file!)
        db_file = f"instant_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        print(f"📁 Creating database: {db_file}")
        
        with create_sqlite_crud(db_file) as crud:
            
            print("✅ Database connection established (no server needed!)")
            
            # Create sample data
            print("\n📊 Creating sample data...")
            
            sample_data = pd.DataFrame({
                'id': range(1, 11),
                'name': [f'User {i}' for i in range(1, 11)],
                'email': [f'user{i}@example.com' for i in range(1, 11)],
                'department': np.random.choice(['IT', 'HR', 'Sales'], 10),
                'salary': np.random.randint(50000, 100000, 10),
                'active': np.random.choice([True, False], 10, p=[0.8, 0.2])
            })
            
            print(f"Generated {len(sample_data)} sample records")
            
            # INSERT data using pandas to_sql
            print("\n📥 Inserting data (CREATE operation)...")
            crud.insert_dataframe(sample_data, "users", if_exists="replace")
            print("✅ Data inserted successfully!")
            
            # READ data
            print("\n📤 Reading data (READ operation)...")
            all_users = crud.read_table("users")
            print(f"📊 Retrieved {len(all_users)} users")
            print("\nSample records:")
            print(all_users[['name', 'department', 'salary', 'active']].head())
            
            # READ with conditions
            print("\n🔍 Finding active IT users...")
            it_users = crud.read_with_conditions(
                "users",
                conditions={"department": "IT", "active": True}
            )
            print(f"Found {len(it_users)} active IT users")
            if not it_users.empty:
                print(it_users[['name', 'email', 'salary']])
            
            # UPDATE data
            print("\n🔄 Giving raises to IT department (UPDATE operation)...")
            updated_count = crud.update_records(
                table_name="users",
                set_values={"salary": 75000},
                conditions={"department": "IT"}
            )
            print(f"✅ Updated salary for {updated_count} IT employees")
            
            # Custom query for analytics
            print("\n📊 Department analysis (Custom SQL)...")
            analysis = crud.read_query("""
                SELECT 
                    department,
                    COUNT(*) as employee_count,
                    ROUND(AVG(salary), 2) as avg_salary,
                    SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END) as active_count
                FROM users 
                GROUP BY department
                ORDER BY avg_salary DESC
            """)
            
            print("Department Analysis:")
            print(analysis)
            
            # DELETE inactive users
            print("\n🗑️ Removing inactive users (DELETE operation)...")
            deleted_count = crud.delete_records(
                table_name="users", 
                conditions={"active": False}
            )
            print(f"✅ Removed {deleted_count} inactive users")
            
            # Final statistics
            final_count = crud.get_row_count("users")
            print(f"\n📊 Final user count: {final_count}")
            
            # Table information
            print("\n📋 Table structure:")
            table_info = crud.get_table_info("users")
            print(table_info[['column_name', 'data_type']])
            
            print(f"\n🎉 Demo completed successfully!")
            print(f"💾 Database saved as: {os.path.abspath(db_file)}")
            print("💡 You can open this file with any SQLite browser or continue using it with the framework")
            
            return True
            
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def show_next_steps():
    """Show available options and next steps."""
    
    print("\n🎯 WHAT'S NEXT?")
    print("=" * 20)
    
    print("\n1️⃣ CONTINUE WITH SQLITE (Recommended)")
    print("   • No server setup required")
    print("   • Perfect for development and testing")
    print("   • Run: python opensource_crud_examples.py")
    
    print("\n2️⃣ TRY IN-MEMORY DATABASE")
    print("   • Ultra-fast temporary database")
    print("   • Perfect for unit tests")
    print("   • No files created")
    
    print("\n3️⃣ EXPLORE FREE CLOUD DATABASES") 
    print("   • Supabase (PostgreSQL) - 500MB free")
    print("   • Railway (PostgreSQL) - Free tier")
    print("   • ElephantSQL - 20MB free")
    print("   • See opensource_db_config.py for setup")
    
    print("\n4️⃣ AVAILABLE SCRIPTS")
    print("   • opensource_crud_examples.py - Complete demos")
    print("   • universal_crud_framework.py - Main framework")
    print("   • opensource_db_config.py - Database configurations")
    
    print("\n📚 FRAMEWORK FEATURES")
    print("   ✅ Complete CRUD operations")
    print("   ✅ pandas DataFrame integration")
    print("   ✅ Multiple database support (SQLite, PostgreSQL, MySQL)")
    print("   ✅ CSV import/export")
    print("   ✅ Professional logging")
    print("   ✅ No localhost setup required")
    
    print("\n💻 QUICK USAGE EXAMPLE:")
    print("""
from universal_crud_framework import create_sqlite_crud
import pandas as pd

# Create database (just a file!)
with create_sqlite_crud("my_data.db") as crud:
    
    # Insert DataFrame
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})
    crud.insert_dataframe(df, "people")
    
    # Query data  
    result = crud.read_table("people")
    print(result)
    """)

def main():
    """Main function - run the instant database demo."""
    
    print("🌟 OPEN SOURCE DATABASE QUICK START")
    print("==================================")
    print("🚀 No server setup required!")
    print("✨ Works instantly with SQLite!")
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install required packages first:")
        print("pip install pandas numpy sqlalchemy")
        return False
    
    print("\n" + "="*40)
    
    # Run instant demo
    success = instant_sqlite_demo()
    
    if success:
        # Show next steps
        show_next_steps()
        
        print("\n✅ INSTANT DATABASE DEMO COMPLETED!")
        print("🎉 You successfully performed CRUD operations without any server setup!")
        
        return True
    else:
        print("\n❌ Demo failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    """
    Run the instant database demo.
    
    This demonstrates:
    - SQLite database operations (no server required)
    - Complete CRUD operations  
    - pandas integration
    - Professional framework usage
    
    Perfect for immediate testing without any setup!
    """
    
    try:
        success = main()
        
        if not success:
            print("\n💡 Troubleshooting:")
            print("• Make sure pandas, numpy, and sqlalchemy are installed")
            print("• Check that you're in the correct directory")
            print("• Verify all framework files are present")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("\n💡 Try installing required packages:")
        print("pip install pandas numpy sqlalchemy")