#!/usr/bin/env python3
"""
🎯 Pandas Multiple Conditions - Quick Demo
==========================================

Simple demonstration of multiple conditions in pandas with
sample data generation and practical examples.

Features:
- Generates sample business data
- Demonstrates 10+ filtering techniques
- Shows performance comparisons
- Includes common mistakes and solutions

Run this for immediate pandas conditions demo!
"""

import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta


def create_sample_data(rows=50000):
    """🚀 Create sample business dataset"""
    print(f"🚀 Creating sample dataset with {rows:,} rows...")
    
    np.random.seed(42)  # Reproducible results
    
    data = {
        # IDs and basics
        'customer_id': range(1, rows + 1),
        'order_id': np.random.randint(100000, 999999, rows),
        
        # Financial data
        'amount': np.round(np.random.lognormal(7, 1, rows), 2),
        'profit': np.round(np.random.lognormal(5, 0.8, rows), 2),
        'cost': np.round(np.random.lognormal(6, 0.9, rows), 2),
        
        # Categories
        'country': np.random.choice(['USA', 'UK', 'Germany', 'France', 'Japan'], rows),
        'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Books'], rows),
        'status': np.random.choice(['ACTIVE', 'PENDING', 'COMPLETED', 'CANCELLED'], rows),
        
        # Scores and quantities
        'score': np.round(np.random.uniform(0, 100, rows), 1),
        'quantity': np.random.randint(1, 100, rows),
        'rating': np.random.randint(1, 6, rows),
        
        # Dates
        'order_date': [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(rows)],
        
        # Boolean flags
        'is_premium': np.random.choice([True, False], rows),
        'is_new_customer': np.random.choice([True, False], rows, p=[0.3, 0.7])
    }
    
    df = pd.DataFrame(data)
    
    # Add derived columns
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    df['profit_margin'] = (df['profit'] / df['amount']) * 100
    
    print(f"✅ Sample data created: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def demo_basic_and_conditions(df):
    """🔹 1. Basic AND Conditions"""
    print("\n🔹 1. BASIC AND CONDITIONS (&)")
    print("-" * 40)
    
    start_time = time.time()
    
    # High-value orders
    result = df[(df['amount'] > 1000) & (df['status'] == 'COMPLETED')]
    
    elapsed = time.time() - start_time
    
    print(f"📊 Condition: (amount > 1000) & (status == 'COMPLETED')")
    print(f"📈 Results: {len(result):,} rows ({len(result)/len(df)*100:.1f}%)")
    print(f"⏱️ Time: {elapsed:.4f}s")
    print(f"💰 Avg amount: ${result['amount'].mean():,.2f}" if len(result) > 0 else "💰 No results")


def demo_or_conditions(df):
    """🔹 2. OR Conditions"""
    print("\n🔹 2. OR CONDITIONS (|)")
    print("-" * 40)
    
    start_time = time.time()
    
    # USA or UK customers
    result = df[(df['country'] == 'USA') | (df['country'] == 'UK')]
    
    elapsed = time.time() - start_time
    
    print(f"📊 Condition: (country == 'USA') | (country == 'UK')")
    print(f"📈 Results: {len(result):,} rows")
    print(f"⏱️ Time: {elapsed:.4f}s")
    
    if len(result) > 0:
        country_counts = result['country'].value_counts()
        print(f"🌍 USA: {country_counts.get('USA', 0):,}, UK: {country_counts.get('UK', 0):,}")


def demo_complex_conditions(df):
    """🔹 3. Complex Mixed (AND + OR)"""
    print("\n🔹 3. COMPLEX MIXED CONDITIONS")
    print("-" * 40)
    
    start_time = time.time()
    
    # High-value electronics or premium customers  
    result = df[
        (df['amount'] > 500) & 
        ((df['category'] == 'Electronics') | (df['is_premium'] == True)) &
        (df['score'] > 70)
    ]
    
    elapsed = time.time() - start_time
    
    print(f"📊 High-value electronics OR premium customers with good scores")
    print(f"📈 Results: {len(result):,} rows")
    print(f"⏱️ Time: {elapsed:.4f}s")
    
    if len(result) > 0:
        print(f"💼 Electronics: {(result['category'] == 'Electronics').sum():,}")
        print(f"⭐ Premium: {result['is_premium'].sum():,}")


def demo_isin_method(df):
    """🔹 4. Using .isin() Method"""
    print("\n🔹 4. USING .isin() METHOD")
    print("-" * 40)
    
    start_time = time.time()
    
    # Multiple categories
    target_categories = ['Electronics', 'Clothing', 'Home']
    result = df[df['category'].isin(target_categories)]
    
    elapsed = time.time() - start_time
    
    print(f"📊 Categories: {target_categories}")
    print(f"📈 Results: {len(result):,} rows")
    print(f"⏱️ Time: {elapsed:.4f}s")
    
    if len(result) > 0:
        category_breakdown = result['category'].value_counts()
        for cat in target_categories:
            print(f"📦 {cat}: {category_breakdown.get(cat, 0):,}")


def demo_between_method(df):
    """🔹 5. Using .between() Method"""
    print("\n🔹 5. USING .between() METHOD")
    print("-" * 40)
    
    start_time = time.time()
    
    # Amount ranges
    result = df[df['amount'].between(500, 2000)]
    
    elapsed = time.time() - start_time
    
    print(f"📊 Amount between $500 - $2000")
    print(f"📈 Results: {len(result):,} rows")
    print(f"⏱️ Time: {elapsed:.4f}s")
    
    if len(result) > 0:
        print(f"💰 Min: ${result['amount'].min():,.2f}")
        print(f"💰 Max: ${result['amount'].max():,.2f}")
        print(f"💰 Avg: ${result['amount'].mean():,.2f}")


def demo_query_method(df):
    """🔹 6. Using .query() Method"""
    print("\n🔹 6. USING .query() METHOD (CLEAN SYNTAX)")
    print("-" * 40)
    
    start_time = time.time()
    
    # Clean query syntax
    result = df.query('amount > 1000 and country in ["USA", "UK"] and score >= 80')
    
    elapsed = time.time() - start_time
    
    print(f"📊 Query: amount > 1000 and country in ['USA', 'UK'] and score >= 80")
    print(f"📈 Results: {len(result):,} rows")
    print(f"⏱️ Time: {elapsed:.4f}s")
    
    if len(result) > 0:
        print(f"🎯 Avg score: {result['score'].mean():.1f}")
        print(f"💰 Total value: ${result['amount'].sum():,.2f}")


def demo_np_where(df):
    """🔹 7. Advanced np.where"""
    print("\n🔹 7. ADVANCED np.where WITH CONDITIONS")
    print("-" * 40)
    
    start_time = time.time()
    
    # Create customer segments
    df['segment'] = np.where(
        (df['amount'] > 2000) & (df['is_premium'] == True),
        'VIP',
        np.where(
            (df['amount'] > 1000) & (df['score'] > 70),
            'Premium', 
            'Standard'
        )
    )
    
    elapsed = time.time() - start_time
    
    print(f"⚙️ Created customer segments based on amount and premium status")
    print(f"⏱️ Time: {elapsed:.4f}s")
    
    segment_counts = df['segment'].value_counts()
    print(f"📊 Segment distribution:")
    for segment, count in segment_counts.items():
        print(f"   {segment}: {count:,} ({count/len(df)*100:.1f}%)")


def demo_negation(df):
    """🔹 8. Negation (NOT ~)"""
    print("\n🔹 8. NEGATION CONDITIONS (NOT ~)")
    print("-" * 40)
    
    start_time = time.time()
    
    # Exclude cancelled and low amounts
    result = df[~((df['status'] == 'CANCELLED') | (df['amount'] < 100))]
    
    elapsed = time.time() - start_time
    
    excluded = len(df) - len(result)
    
    print(f"📊 Excluded: Cancelled orders OR amounts < $100")
    print(f"📈 Remaining: {len(result):,} rows")
    print(f"🚫 Excluded: {excluded:,} rows ({excluded/len(df)*100:.1f}%)")
    print(f"⏱️ Time: {elapsed:.4f}s")


def demo_loc_method(df):
    """🔹 9. Using .loc with conditions"""
    print("\n🔹 9. USING .loc WITH CONDITIONS")
    print("-" * 40)
    
    start_time = time.time()
    
    # Select specific columns with conditions
    result = df.loc[
        (df['amount'] > 1500) & (df['score'] > 80),
        ['customer_id', 'amount', 'score', 'country', 'category']
    ]
    
    elapsed = time.time() - start_time
    
    print(f"📊 High-value, high-score customers (selected columns)")
    print(f"📈 Results: {len(result):,} rows × {len(result.columns)} columns")
    print(f"⏱️ Time: {elapsed:.4f}s")
    
    if len(result) > 0:
        print(f"🎯 Avg amount: ${result['amount'].mean():,.2f}")
        print(f"⭐ Avg score: {result['score'].mean():.1f}")


def demo_performance_comparison(df):
    """🔹 10. Performance Comparison"""
    print("\n🔹 10. PERFORMANCE COMPARISON")
    print("-" * 40)
    
    # Same logic, different methods
    condition_desc = "amount > 1000 AND country == 'USA' AND score > 70"
    
    methods = {}
    
    # Method 1: Boolean indexing
    start_time = time.time()
    result1 = df[(df['amount'] > 1000) & (df['country'] == 'USA') & (df['score'] > 70)]
    methods['Boolean Indexing'] = time.time() - start_time
    
    # Method 2: Query method  
    start_time = time.time()
    result2 = df.query('amount > 1000 and country == "USA" and score > 70')
    methods['Query Method'] = time.time() - start_time
    
    # Method 3: Step-by-step
    start_time = time.time()
    temp1 = df[df['amount'] > 1000]
    temp2 = temp1[temp1['country'] == 'USA']
    result3 = temp2[temp2['score'] > 70]
    methods['Step-by-step'] = time.time() - start_time
    
    print(f"📊 Condition: {condition_desc}")
    print(f"📈 Results: {len(result1):,} rows (all methods)")
    print(f"\n⏱️ Performance ranking:")
    
    sorted_methods = sorted(methods.items(), key=lambda x: x[1])
    
    for i, (method, time_taken) in enumerate(sorted_methods, 1):
        speed_ratio = sorted_methods[0][1] / time_taken
        print(f"   {i}. {method:<18}: {time_taken:.5f}s ({speed_ratio:.1f}x)")
    
    # Verify identical results
    identical = len(result1) == len(result2) == len(result3)
    print(f"✅ Results identical: {identical}")


def show_common_mistakes():
    """⚠️ Common Mistakes to Avoid"""
    print("\n⚠️ COMMON MISTAKES TO AVOID")
    print("-" * 40)
    
    print("❌ WRONG syntax:")
    print("   df[df['col1'] > 100 and df['col2'] < 200]  # Python 'and'")
    print("   df[df['col1'] > 100 & df['col2'] < 200]    # Missing brackets")
    
    print("\n✅ CORRECT syntax:")
    print("   df[(df['col1'] > 100) & (df['col2'] < 200)]  # Use & with brackets")
    
    print("\n💡 Key rules:")
    print("   • Use & instead of 'and'")
    print("   • Use | instead of 'or'") 
    print("   • Use ~ for NOT/negation")
    print("   • Always use brackets around each condition")
    print("   • Use .isin() for multiple value matching")
    print("   • Use .between() for ranges")


def run_pandas_conditions_demo():
    """🚀 Main demo runner"""
    print("🎯 PANDAS MULTIPLE CONDITIONS - QUICK DEMO")
    print("=" * 50)
    
    # Create sample data
    df = create_sample_data(50000)
    
    # Run all demos
    demos = [
        demo_basic_and_conditions,
        demo_or_conditions,
        demo_complex_conditions,
        demo_isin_method,
        demo_between_method,
        demo_query_method,
        demo_np_where,
        demo_negation,
        demo_loc_method,
        demo_performance_comparison
    ]
    
    for demo_func in demos:
        try:
            demo_func(df)
            time.sleep(0.3)  # Brief pause
        except Exception as e:
            print(f"❌ {demo_func.__name__} failed: {str(e)}")
    
    # Show common mistakes
    show_common_mistakes()
    
    # Final summary
    print(f"\n🎉 DEMO COMPLETED")
    print(f"=" * 30)
    print(f"📊 Dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"🎯 Techniques demonstrated: 10+")
    print(f"💡 Key takeaway: Always use & with brackets for AND conditions!")
    
    # Show sample of the final data
    print(f"\n📋 Sample data with segments:")
    sample_cols = ['customer_id', 'amount', 'score', 'country', 'segment']
    print(df[sample_cols].head(5).to_string(index=False))


if __name__ == "__main__":
    run_pandas_conditions_demo()