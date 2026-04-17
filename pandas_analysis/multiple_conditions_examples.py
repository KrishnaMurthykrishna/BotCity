#!/usr/bin/env python3
"""
🎯 Pandas Multiple Conditions - Advanced Examples
================================================

Comprehensive examples of multiple condition filtering in pandas
with performance benchmarking on large datasets.

Features:
- Multiple AND/OR conditions
- Complex nested conditions  
- Performance comparisons
- Memory-efficient filtering
- Real business scenarios
- np.where advanced usage

Author: AI Assistant
Date: 2024-04-10
"""

import pandas as pd
import numpy as np
import time
from typing import Dict, List, Tuple, Any
import os
import gc


class PandasConditionsExpert:
    """🚀 Advanced pandas filtering with multiple conditions"""
    
    def __init__(self, csv_file: str):
        """Initialize with dataset"""
        self.csv_file = csv_file
        self.df = None
        self.results = {}
        
    def load_dataset(self, sample_size: int = None) -> bool:
        """📂 Load dataset with optional sampling"""
        try:
            print(f"📂 Loading dataset: {os.path.basename(self.csv_file)}")
            
            if sample_size:
                print(f"🎯 Sampling {sample_size:,} rows for faster testing...")
                # Read a sample for faster testing
                total_lines = sum(1 for line in open(self.csv_file)) - 1  # -1 for header
                skip_rows = sorted(np.random.choice(range(1, total_lines), 
                                                  total_lines - sample_size, 
                                                  replace=False))
                self.df = pd.read_csv(self.csv_file, skiprows=skip_rows)
            else:
                self.df = pd.read_csv(self.csv_file)
            
            print(f"✅ Dataset loaded: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
            print(f"💾 Memory usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load dataset: {str(e)}")
            return False
    
    def demo_basic_conditions(self):
        """🔹 1. Basic Multiple Conditions (AND &)"""
        print("\n🔹 1. BASIC MULTIPLE CONDITIONS (AND &)")
        print("-" * 50)
        
        # Financial filtering
        start_time = time.time()
        
        condition = "(df['amount_1'] > 1000) & (df['amount_2'] < 5000)"
        result_df = self.df[(self.df['amount_1'] > 1000) & (self.df['amount_2'] < 5000)]
        
        elapsed = time.time() - start_time
        
        print(f"📊 Condition: {condition}")
        print(f"📈 Results: {len(result_df):,} rows ({len(result_df)/len(self.df)*100:.1f}%)")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        # Show sample results
        if not result_df.empty:
            print(f"💰 Sample amounts:")
            sample = result_df[['amount_1', 'amount_2']].head(3)
            for idx, row in sample.iterrows():
                print(f"   Amount1: ${row['amount_1']:,.2f}, Amount2: ${row['amount_2']:,.2f}")
        
        self.results['basic_and'] = {'count': len(result_df), 'time': elapsed}
    
    def demo_or_conditions(self):
        """🔹 2. OR Conditions"""
        print("\n🔹 2. OR CONDITIONS")
        print("-" * 50)
        
        start_time = time.time()
        
        condition = "(df['country'] == 'USA') | (df['country'] == 'UK')"
        result_df = self.df[(self.df['country'] == 'USA') | (self.df['country'] == 'UK')]
        
        elapsed = time.time() - start_time
        
        print(f"📊 Condition: {condition}")
        print(f"📈 Results: {len(result_df):,} rows")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        # Country breakdown
        if not result_df.empty:
            country_counts = result_df['country'].value_counts()
            print(f"🌍 Country breakdown:")
            for country, count in country_counts.head().items():
                print(f"   {country}: {count:,} rows")
        
        self.results['basic_or'] = {'count': len(result_df), 'time': elapsed}
    
    def demo_complex_conditions(self):
        """🔹 3. Complex Mixed (AND + OR)"""
        print("\n🔹 3. COMPLEX MIXED CONDITIONS")
        print("-" * 50)
        
        start_time = time.time()
        
        # Complex business logic
        condition = """
        (df['amount_1'] > 2000) & 
        ((df['country'] == 'USA') | (df['country'] == 'UK')) & 
        (df['order_status'] == 'COMPLETED') & 
        (df['score_1'] > 75)
        """
        
        result_df = self.df[
            (self.df['amount_1'] > 2000) & 
            ((self.df['country'] == 'USA') | (self.df['country'] == 'UK')) & 
            (self.df['order_status'] == 'COMPLETED') & 
            (self.df['score_1'] > 75)
        ]
        
        elapsed = time.time() - start_time
        
        print(f"📊 Complex Condition: High-value completed orders from US/UK with good scores")
        print(f"📈 Results: {len(result_df):,} rows")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        if not result_df.empty:
            print(f"💼 Business insights:")
            print(f"   • Avg amount: ${result_df['amount_1'].mean():,.2f}")
            print(f"   • Avg score: {result_df['score_1'].mean():.1f}")
            
            country_revenue = result_df.groupby('country')['amount_1'].sum()
            for country, revenue in country_revenue.items():
                print(f"   • {country} revenue: ${revenue:,.2f}")
        
        self.results['complex_mixed'] = {'count': len(result_df), 'time': elapsed}
    
    def demo_isin_conditions(self):
        """🔹 4. Using .isin() for Multiple Values"""
        print("\n🔹 4. USING .isin() FOR MULTIPLE VALUES")
        print("-" * 50)
        
        start_time = time.time()
        
        # Multiple category filtering
        target_categories = ['Electronics', 'Clothing', 'Home']
        result_df = self.df[self.df['category_name'].isin(target_categories)]
        
        elapsed = time.time() - start_time
        
        print(f"📊 Categories: {target_categories}")
        print(f"📈 Results: {len(result_df):,} rows")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        if not result_df.empty:
            category_stats = result_df.groupby('category_name').agg({
                'amount_1': ['count', 'mean', 'sum']
            }).round(2)
            
            print(f"📊 Category statistics:")
            for category in target_categories:
                if category in result_df['category_name'].values:
                    cat_data = result_df[result_df['category_name'] == category]
                    print(f"   {category}: {len(cat_data):,} orders, avg ${cat_data['amount_1'].mean():.2f}")
        
        self.results['isin_method'] = {'count': len(result_df), 'time': elapsed}
    
    def demo_between_conditions(self):
        """🔹 5. Using .between() for Ranges"""
        print("\n🔹 5. USING .between() FOR RANGES")
        print("-" * 50)
        
        start_time = time.time()
        
        # Date and amount ranges
        result_df = self.df[
            (self.df['amount_1'].between(1000, 5000)) & 
            (self.df['score_1'].between(60, 90))
        ]
        
        elapsed = time.time() - start_time
        
        print(f"📊 Condition: Amount between $1K-$5K AND Score between 60-90")
        print(f"📈 Results: {len(result_df):,} rows")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        if not result_df.empty:
            print(f"📊 Range statistics:")
            print(f"   • Amount range: ${result_df['amount_1'].min():.2f} - ${result_df['amount_1'].max():.2f}")
            print(f"   • Score range: {result_df['score_1'].min():.1f} - {result_df['score_1'].max():.1f}")
            print(f"   • Median amount: ${result_df['amount_1'].median():.2f}")
        
        self.results['between_method'] = {'count': len(result_df), 'time': elapsed}
    
    def demo_query_method(self):
        """🔹 6. Using .query() Method (Cleaner Syntax)"""
        print("\n🔹 6. USING .query() METHOD (CLEANER SYNTAX)")
        print("-" * 50)
        
        start_time = time.time()
        
        # Clean query syntax
        query_string = """
        amount_1 > 1500 and 
        country in ['USA', 'UK', 'Germany'] and 
        order_status == 'COMPLETED' and 
        score_1 >= 70
        """
        
        result_df = self.df.query(query_string)
        
        elapsed = time.time() - start_time
        
        print(f"📊 Query: {query_string.strip()}")
        print(f"📈 Results: {len(result_df):,} rows")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        if not result_df.empty:
            print(f"🎯 Query results summary:")
            summary = result_df.groupby('country').agg({
                'amount_1': ['count', 'sum'],
                'score_1': 'mean'
            }).round(2)
            
            for country in ['USA', 'UK', 'Germany']:
                if country in result_df['country'].values:
                    country_data = result_df[result_df['country'] == country]
                    print(f"   {country}: {len(country_data):,} orders, total ${country_data['amount_1'].sum():,.2f}")
        
        self.results['query_method'] = {'count': len(result_df), 'time': elapsed}
    
    def demo_np_where_conditions(self):
        """🔹 7. Advanced np.where with Multiple Conditions"""
        print("\n🔹 7. ADVANCED np.where WITH MULTIPLE CONDITIONS")  
        print("-" * 50)
        
        start_time = time.time()
        
        # Create performance categories
        self.df['performance_category'] = np.where(
            (self.df['amount_1'] > 3000) & (self.df['score_1'] > 80),
            'High Performer',
            np.where(
                (self.df['amount_1'] > 1000) & (self.df['score_1'] > 60),
                'Medium Performer',
                'Standard'
            )
        )
        
        elapsed = time.time() - start_time
        
        print(f"⚙️ Created performance categories based on amount and score")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        # Performance breakdown
        perf_counts = self.df['performance_category'].value_counts()
        print(f"📊 Performance Distribution:")
        for category, count in perf_counts.items():
            percentage = (count / len(self.df)) * 100
            print(f"   {category}: {count:,} ({percentage:.1f}%)")
        
        # Advanced conditional calculation
        self.df['bonus_eligible'] = np.where(
            (self.df['performance_category'] == 'High Performer') & 
            (self.df['order_status'] == 'COMPLETED') & 
            (self.df['country'].isin(['USA', 'UK'])),
            self.df['amount_1'] * 0.05,  # 5% bonus
            0
        )
        
        bonus_total = self.df['bonus_eligible'].sum()
        bonus_recipients = (self.df['bonus_eligible'] > 0).sum()
        
        print(f"💰 Bonus Program Results:")
        print(f"   • Eligible recipients: {bonus_recipients:,}")
        print(f"   • Total bonus pool: ${bonus_total:,.2f}")
        print(f"   • Avg bonus: ${bonus_total/bonus_recipients:.2f}" if bonus_recipients > 0 else "   • Avg bonus: $0.00")
        
        self.results['np_where_advanced'] = {
            'categories': len(perf_counts),
            'bonus_recipients': bonus_recipients,
            'time': elapsed
        }
    
    def demo_negation_conditions(self):
        """🔹 8. Negation Conditions (NOT ~)"""
        print("\n🔹 8. NEGATION CONDITIONS (NOT ~)")
        print("-" * 50)
        
        start_time = time.time()
        
        # Exclude specific conditions
        excluded_df = self.df[
            ~(
                (self.df['order_status'] == 'CANCELLED') | 
                (self.df['amount_1'] < 100) |
                (self.df['country'] == 'China')
            )
        ]
        
        elapsed = time.time() - start_time
        
        print(f"📊 Excluded: Cancelled orders, small amounts (<$100), China orders")
        print(f"📈 Remaining: {len(excluded_df):,} rows ({len(excluded_df)/len(self.df)*100:.1f}%)")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        # What was excluded
        excluded_count = len(self.df) - len(excluded_df)
        print(f"🚫 Excluded: {excluded_count:,} rows ({excluded_count/len(self.df)*100:.1f}%)")
        
        # Breakdown of exclusions
        cancelled = (self.df['order_status'] == 'CANCELLED').sum()
        small_amounts = (self.df['amount_1'] < 100).sum()
        china_orders = (self.df['country'] == 'China').sum()
        
        print(f"🔍 Exclusion breakdown:")
        print(f"   • Cancelled orders: {cancelled:,}")
        print(f"   • Small amounts: {small_amounts:,}")
        print(f"   • China orders: {china_orders:,}")
        
        self.results['negation'] = {'remaining': len(excluded_df), 'time': elapsed}
    
    def demo_loc_with_conditions(self):
        """🔹 9. Using .loc with Multiple Conditions"""
        print("\n🔹 9. USING .loc WITH MULTIPLE CONDITIONS")
        print("-" * 50)
        
        start_time = time.time()
        
        # Select specific columns with conditions
        result_df = self.df.loc[
            (self.df['amount_1'] > 2000) & 
            (self.df['score_1'] > 80) & 
            (self.df['country'].isin(['USA', 'UK'])),
            ['customer_id', 'amount_1', 'score_1', 'country', 'order_status']
        ]
        
        elapsed = time.time() - start_time
        
        print(f"📊 High-value, high-score US/UK customers")
        print(f"📈 Results: {len(result_df):,} rows × {len(result_df.columns)} columns")
        print(f"⏱️ Time: {elapsed:.3f}s")
        
        if not result_df.empty:
            print(f"🎯 Premium customer insights:")
            print(f"   • Avg amount: ${result_df['amount_1'].mean():,.2f}")
            print(f"   • Avg score: {result_df['score_1'].mean():.1f}")
            
            # Status distribution
            status_dist = result_df['order_status'].value_counts()
            for status, count in status_dist.head(3).items():
                print(f"   • {status}: {count:,}")
        
        self.results['loc_method'] = {'count': len(result_df), 'time': elapsed}
    
    def demo_performance_comparison(self):
        """🔹 10. Performance Comparison: Different Methods"""
        print("\n🔹 10. PERFORMANCE COMPARISON")
        print("-" * 50)
        
        # Same condition, different methods
        condition_logic = "(amount_1 > 1000) & (country == 'USA') & (score_1 > 70)"
        
        methods = {}
        
        # Method 1: Standard boolean indexing
        start_time = time.time()
        result1 = self.df[
            (self.df['amount_1'] > 1000) & 
            (self.df['country'] == 'USA') & 
            (self.df['score_1'] > 70)
        ]
        methods['Boolean Indexing'] = time.time() - start_time
        
        # Method 2: Query method
        start_time = time.time()
        result2 = self.df.query('amount_1 > 1000 and country == "USA" and score_1 > 70')
        methods['Query Method'] = time.time() - start_time
        
        # Method 3: Multiple steps
        start_time = time.time()
        temp_df = self.df[self.df['amount_1'] > 1000]
        temp_df = temp_df[temp_df['country'] == 'USA']
        result3 = temp_df[temp_df['score_1'] > 70]
        methods['Step-by-step'] = time.time() - start_time
        
        print(f"📊 Condition: {condition_logic}")
        print(f"📈 Results: {len(result1):,} rows (all methods should match)")
        print(f"\n⏱️ Performance Comparison:")
        
        sorted_methods = sorted(methods.items(), key=lambda x: x[1])
        
        for i, (method, time_taken) in enumerate(sorted_methods, 1):
            speed_factor = sorted_methods[0][1] / time_taken
            print(f"   {i}. {method:<20}: {time_taken:.4f}s ({speed_factor:.1f}x)")
        
        # Verify results are identical
        identical = len(result1) == len(result2) == len(result3)
        print(f"✅ Results identical: {identical}")
        
        self.results['performance'] = methods
    
    def run_all_demos(self, sample_size: int = 100000):
        """🚀 Run all condition demos"""
        print("🎯 PANDAS MULTIPLE CONDITIONS - COMPREHENSIVE DEMO")
        print("=" * 60)
        
        if not self.load_dataset(sample_size):
            return
        
        # Run all demos
        demos = [
            self.demo_basic_conditions,
            self.demo_or_conditions, 
            self.demo_complex_conditions,
            self.demo_isin_conditions,
            self.demo_between_conditions,
            self.demo_query_method,
            self.demo_np_where_conditions,
            self.demo_negation_conditions,
            self.demo_loc_with_conditions,
            self.demo_performance_comparison
        ]
        
        for demo in demos:
            try:
                demo()
                time.sleep(0.5)  # Brief pause between demos
            except Exception as e:
                print(f"❌ Demo failed: {str(e)}")
        
        # Final summary
        self._print_summary()
    
    def _print_summary(self):
        """📊 Print execution summary"""
        print("\n🎯 EXECUTION SUMMARY")
        print("=" * 40)
        
        total_operations = len(self.results)
        print(f"📊 Operations completed: {total_operations}")
        print(f"📂 Dataset size: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
        
        # Time summary  
        time_results = {k: v.get('time', 0) for k, v in self.results.items() if 'time' in v}
        if time_results:
            total_time = sum(time_results.values())
            fastest = min(time_results.items(), key=lambda x: x[1])
            slowest = max(time_results.items(), key=lambda x: x[1])
            
            print(f"⏱️ Total time: {total_time:.3f}s")
            print(f"🚀 Fastest operation: {fastest[0]} ({fastest[1]:.4f}s)")
            print(f"🐌 Slowest operation: {slowest[0]} ({slowest[1]:.4f}s)")


def run_conditions_demo():
    """🚀 Main function to run conditions demo"""
    
    # Check if dataset exists
    csv_file = "business_data_1M_100cols.csv"
    
    if not os.path.exists(csv_file):
        print("📂 Dataset not found. Generating sample dataset...")
        from large_dataset_generator import generate_large_dataset
        csv_file = generate_large_dataset()
        
        if not csv_file:
            print("❌ Failed to generate dataset")
            return
    
    # Run demos
    expert = PandasConditionsExpert(csv_file)
    expert.run_all_demos(sample_size=100000)  # Use 100k sample for faster demo


