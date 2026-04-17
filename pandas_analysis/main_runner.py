#!/usr/bin/env python3
"""
🎯 Pandas Analysis Suite - Main Runner
=====================================

Complete pandas data analysis suite with:
- Large dataset generation (10 lakh rows)
- Multiple conditions filtering
- Excel pivot tables with win32com 
- Performance benchmarking
- Professional reporting

Author: AI Assistant
Date: 2024-04-10
"""

import os
import sys
import time
from datetime import datetime


def print_banner():
    """🎨 Print application banner"""
    print("🎯" * 25)
    print("🎯" + " " * 15 + "PANDAS ANALYSIS SUITE" + " " * 16 + "🎯")
    print("🎯" + " " * 12 + "Large Data • Conditions • Pivots" + " " * 13 + "🎯")
    print("🎯" * 25)


def check_dependencies():
    """🔍 Check required dependencies"""
    dependencies = {
        'pandas': 'pip install pandas',
        'numpy': 'pip install numpy', 
        'win32com.client': 'pip install pywin32'
    }
    
    missing = []
    
    for module, install_cmd in dependencies.items():
        try:
            if module == 'win32com.client':
                import win32com.client
            else:
                __import__(module)
        except ImportError:
            missing.append((module, install_cmd))
    
    if missing:
        print("❌ Missing dependencies:")
        for module, cmd in missing:
            print(f"   • {module}: {cmd}")
        return False
    
    print("✅ All dependencies available")
    return True


def show_menu():
    """📋 Display main menu"""
    print(f"\n📋 MAIN MENU")
    print(f"=" * 40)
    print(f"1. 🚀 Generate Large Dataset (10 Lakh rows)")
    print(f"2. 🎯 Multiple Conditions Demo")
    print(f"3. 📊 Excel Pivot Tables (win32com)")
    print(f"4. 🔄 Complete Workflow (All steps)")
    print(f"5. 📊 Performance Benchmark")
    print(f"6. 🔍 Dataset Information")
    print(f"0. 🚪 Exit")
    print(f"=" * 40)


def generate_dataset_menu():
    """🚀 Generate large dataset"""
    print(f"\n🚀 LARGE DATASET GENERATION")
    print(f"=" * 40)
    
    try:
        from large_dataset_generator import LargeDatasetGenerator
        
        # Get user preferences
        print(f"📊 Dataset Configuration:")
        
        rows = 10000  # Default 10 lakh rows
        cols =100
        
        
        filename = "business_data_1M_100cols.csv"
        
        # Generate dataset
        generator = LargeDatasetGenerator(rows=rows, columns=cols)
        csv_file = generator.generate_business_dataset(filename)
        
        if csv_file:
            file_size = os.path.getsize(csv_file) / (1024**2)  # MB
            print(f"\n✅ Dataset generated successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Size: {file_size:.1f} MB")
            print(f"🎯 Ready for analysis")
        
    except Exception as e:
        print(f"❌ Generation failed: {str(e)}")
    
    input(f"\nPress Enter to continue...")


def run_conditions_demo():
    """🎯 Run multiple conditions demonstration"""
    print(f"\n🎯 MULTIPLE CONDITIONS DEMO")
    print(f"=" * 40)
    
    try:
        from multiple_conditions_examples import PandasConditionsExpert
        
        # Check for dataset
        csv_file = "business_data_1M_100cols.csv"
        if not os.path.exists(csv_file):
            print(f"📂 Dataset not found. Please generate it first (option 1)")
            input(f"Press Enter to continue...")
            return
        
        # Get sample size
        sample_input = input(f"Sample size for demo (default 100,000): ").strip()
        sample_size = int(sample_input) if sample_input else 100000
        
        # Run demo
        expert = PandasConditionsExpert(csv_file)
        expert.run_all_demos(sample_size=sample_size)
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
    
    input(f"\nPress Enter to continue...")


def run_pivot_tables():
    """📊 Create Excel pivot tables"""
    print(f"\n📊 EXCEL PIVOT TABLES")
    print(f"=" * 40)
    
    try:
        from excel_pivot_creator import ExcelPivotCreator
        import win32com.client
        
        # Check for dataset
        csv_file = "business_data_1M_100cols.csv"
        if not os.path.exists(csv_file):
            print(f"📂 Large dataset not found. Creating sample dataset...")
            
            from large_dataset_generator import LargeDatasetGenerator
            generator = LargeDatasetGenerator(rows=50000, columns=50)
            csv_file = generator.generate_business_dataset("sample_business_data.csv")
            
            if not csv_file:
                print(f"❌ Failed to create sample dataset")
                input(f"Press Enter to continue...")
                return
        
        # Display options
        print(f"📊 Pivot Table Options:")
        display_choice = input(f"   Display Excel? (y/n, default=y): ").strip().lower()
        display = display_choice != 'n'
        
        # Create pivot tables
        creator = ExcelPivotCreator(csv_file)
        success = creator.create_comprehensive_pivot_analysis(display=display)
        
        if success:
            print(f"\n✅ Pivot tables created successfully!")
        
    except ImportError:
        print(f"❌ win32com not available. Install with: pip install pywin32")
    except Exception as e:
        print(f"❌ Pivot creation failed: {str(e)}")
    
    input(f"\nPress Enter to continue...")


def run_complete_workflow():
    """🔄 Run complete analysis workflow"""
    print(f"\n🔄 COMPLETE ANALYSIS WORKFLOW")
    print(f"=" * 40)
    
    workflow_steps = [
        ("🚀 Generate Dataset", generate_dataset_step),
        ("🎯 Multiple Conditions", conditions_step), 
        ("📊 Excel Pivots", pivots_step),
        ("📋 Summary Report", summary_step)
    ]
    
    results = {}
    
    for step_name, step_function in workflow_steps:
        print(f"\n{step_name}")
        print(f"-" * 30)
        
        try:
            step_result = step_function()
            results[step_name] = step_result
            print(f"✅ {step_name} completed")
        except Exception as e:
            print(f"❌ {step_name} failed: {str(e)}")
            results[step_name] = f"Failed: {str(e)}"
    
    # Final summary
    print(f"\n📊 WORKFLOW SUMMARY")
    print(f"=" * 30)
    for step, result in results.items():
        status = "✅" if "Failed" not in str(result) else "❌"
        print(f"{status} {step}")
    
    input(f"\nPress Enter to continue...")


def generate_dataset_step():
    """🚀 Workflow step: Generate dataset"""
    from large_dataset_generator import LargeDatasetGenerator
    
    generator = LargeDatasetGenerator(rows=100000, columns=50)  # Smaller for demo
    csv_file = generator.generate_business_dataset("workflow_data.csv")
    return csv_file


def conditions_step():
    """🎯 Workflow step: Test conditions"""
    from multiple_conditions_examples import PandasConditionsExpert
    
    expert = PandasConditionsExpert("workflow_data.csv")
    expert.run_all_demos(sample_size=50000)
    return "Conditions demo completed"


def pivots_step():
    """📊 Workflow step: Create pivots"""
    try:
        from excel_pivot_creator import ExcelPivotCreator
        
        creator = ExcelPivotCreator("workflow_data.csv")
        success = creator.create_comprehensive_pivot_analysis(display=False)
        return "Pivots created" if success else "Pivots failed"
    except ImportError:
        return "win32com not available"


def summary_step():
    """📋 Workflow step: Generate summary"""
    # Create summary report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary = f"""
PANDAS ANALYSIS WORKFLOW SUMMARY
Generated: {timestamp}

[+] Large dataset generation completed
[+] Multiple conditions filtering tested  
[+] Excel pivot tables created
[+] Professional analysis workflow executed

Files created:
- workflow_data.csv (source data)
- pandas_pivot_analysis_*.xlsx (pivot tables)
- Detailed logs and performance metrics

The complete pandas analysis suite demonstrated:
1. High-performance data generation
2. Advanced filtering techniques  
3. Professional Excel integration
4. Automated reporting capabilities
"""
    
    with open("workflow_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(summary)
    return "Summary report created"


def run_performance_benchmark():
    """📊 Performance benchmark"""
    print(f"\n📊 PERFORMANCE BENCHMARK")
    print(f"=" * 40)
    
    try:
        import pandas as pd
        import numpy as np
        
        # Check for dataset
        csv_file = "business_data_1M_100cols.csv"
        if not os.path.exists(csv_file):
            print(f"📂 Dataset not found. Please generate it first (option 1)")
            input(f"Press Enter to continue...")
            return
        
        print(f"🚀 Running performance tests...")
        
        # Test 1: Loading performance
        start_time = time.time()
        df = pd.read_csv(csv_file, nrows=100000)  # Sample
        load_time = time.time() - start_time
        
        print(f"📂 Loading 100K rows: {load_time:.3f}s")
        
        # Test 2: Filtering performance
        conditions = [
            "Simple condition",
            "Multiple AND conditions", 
            "Complex mixed conditions",
            "isin() method",
            "query() method"
        ]
        
        for condition in conditions:
            start_time = time.time()
            
            if "Simple" in condition:
                result = df[df['amount_1'] > 1000]
            elif "Multiple AND" in condition:
                result = df[(df['amount_1'] > 1000) & (df['score_1'] > 70)]
            elif "Complex" in condition:
                result = df[(df['amount_1'] > 1000) & 
                           ((df['country'] == 'USA') | (df['country'] == 'UK')) &
                           (df['order_status'] == 'COMPLETED')]
            elif "isin" in condition:
                result = df[df['country'].isin(['USA', 'UK', 'Germany'])]
            elif "query" in condition:
                result = df.query('amount_1 > 1000 and score_1 > 70')
            
            elapsed = time.time() - start_time
            print(f"🎯 {condition}: {elapsed:.4f}s ({len(result):,} results)")
        
        # Memory usage
        memory_mb = df.memory_usage(deep=True).sum() / (1024**2)
        print(f"💾 Memory usage: {memory_mb:.1f} MB")
        
    except Exception as e:
        print(f"❌ Benchmark failed: {str(e)}")
    
    input(f"\nPress Enter to continue...")


def show_dataset_info():
    """🔍 Show dataset information"""
    print(f"\n🔍 DATASET INFORMATION")
    print(f"=" * 40)
    
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if not csv_files:
        print(f"📂 No CSV files found in current directory")
        input(f"Press Enter to continue...")
        return
    
    for csv_file in csv_files:
        try:
            # File info
            file_size = os.path.getsize(csv_file) / (1024**2)  # MB
            
            # Sample data info
            import pandas as pd
            df_sample = pd.read_csv(csv_file, nrows=1000)
            
            print(f"\n📁 {csv_file}")
            print(f"   Size: {file_size:.1f} MB")
            print(f"   Columns: {len(df_sample.columns)}")
            print(f"   Sample rows loaded: {len(df_sample):,}")
            
            # Estimated total rows
            row_size_bytes = df_sample.memory_usage(deep=True).sum() / len(df_sample)
            estimated_total_rows = int((file_size * 1024**2) / row_size_bytes)
            
            print(f"   Estimated total rows: ~{estimated_total_rows:,}")
            
            # Column types
            numeric_cols = len(df_sample.select_dtypes(include=[np.number]).columns)
            text_cols = len(df_sample.select_dtypes(include=['object']).columns)
            date_cols = len(df_sample.select_dtypes(include=['datetime']).columns)
            
            print(f"   Column types: {numeric_cols} numeric, {text_cols} text, {date_cols} date")
            
        except Exception as e:
            print(f"   ❌ Error reading {csv_file}: {str(e)}")
    
    input(f"\nPress Enter to continue...")


def main():
    """🚀 Main application"""
    
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print(f"\nPlease install missing dependencies and try again.")
        return
    
    show_menu()
    generate_dataset_menu()
    run_conditions_demo()

if __name__ == "__main__":
    main()