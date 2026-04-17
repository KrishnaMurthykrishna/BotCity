#!/usr/bin/env python3
"""
🚀 Large Dataset Generator - 10 Lakh Records, 100 Columns
==========================================================

Generates massive datasets for pandas performance testing and
multiple condition filtering with realistic business data.

Features:
- Creates 1,000,000 rows × 100 columns
- Realistic business data (sales, finance, inventory)
- Memory-optimized generation
- Multiple data types (numeric, categorical, dates)
- Pre-built conditions for filtering
- Progress tracking

Author: AI Assistant
Date: 2024-04-10
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import time
from typing import Dict, List, Tuple
import gc


class LargeDatasetGenerator:
    """🎯 High-performance large dataset generator"""
    
    def __init__(self, rows: int = 1000000, columns: int = 100):
        """
        Initialize generator
        
        Args:
            rows: Number of rows to generate (default: 1M)
            columns: Number of columns to generate (default: 100)
        """
        self.rows = rows
        self.columns = columns
        self.chunk_size = 100000  # Process in chunks of 100k
        
        print(f"🚀 Dataset Generator Initialized")
        print(f"📊 Target Size: {self.rows:,} rows × {self.columns} columns")
        print(f"💾 Estimated Size: ~{(self.rows * self.columns * 8) / (1024**3):.2f} GB")
    
    def generate_business_dataset(self, filename: str = "large_business_data.csv") -> str:
        """
        🏪 Generate realistic business dataset with multiple data types
        
        Returns:
            str: Path to generated CSV file
        """
        print("\n🔧 LARGE BUSINESS DATASET GENERATION")
        print("=" * 50)
        
        start_time = time.time()
        
        # Define business-relevant column structure
        column_config = self._get_business_columns()
        
        print(f"📋 Generating {len(column_config)} business columns...")
        
        # Generate data in chunks to manage memory
        csv_path = filename
        
        try:
            first_chunk = True
            
            for chunk_start in range(0, self.rows, self.chunk_size):
                chunk_end = min(chunk_start + self.chunk_size, self.rows)
                chunk_rows = chunk_end - chunk_start
                
                print(f"⚙️ Processing chunk: {chunk_start+1:,} to {chunk_end:,}")
                
                # Generate chunk data
                chunk_data = self._generate_chunk_data(chunk_rows, column_config, chunk_start)
                
                # Create DataFrame
                df_chunk = pd.DataFrame(chunk_data)
                
                # Write to CSV
                mode = 'w' if first_chunk else 'a'
                header = first_chunk
                
                df_chunk.to_csv(csv_path, mode=mode, header=header, index=False)
                
                first_chunk = False
                
                # Memory cleanup
                del df_chunk, chunk_data
                gc.collect()
                
                # Progress update
                progress = (chunk_end / self.rows) * 100
                elapsed = time.time() - start_time
                
                print(f"📊 Progress: {progress:.1f}% | Time: {elapsed:.1f}s")
        
        except Exception as e:
            print(f"❌ Generation failed: {str(e)}")
            return ""
        
        total_time = time.time() - start_time
        file_size_mb = os.path.getsize(csv_path) / (1024**2)
        
        print(f"\n✅ Dataset Generated Successfully!")
        print(f"📁 File: {csv_path}")
        print(f"📊 Size: {file_size_mb:.1f} MB")
        print(f"⏱️ Time: {total_time:.1f}s")
        print(f"🚀 Speed: {self.rows/total_time:,.0f} rows/second")
        
        return csv_path
    
    def _get_business_columns(self) -> Dict:
        """📋 Define realistic business column structure"""
        
        columns = {}
        
        # Core ID columns (10)
        columns.update({
            'customer_id': 'sequential_id',
            'order_id': 'random_id',
            'product_id': 'random_id',
            'region_id': 'categorical',
            'salesperson_id': 'categorical',
            'store_id': 'categorical',
            'supplier_id': 'categorical',
            'category_id': 'categorical',
            'brand_id': 'categorical',
            'transaction_id': 'random_id'
        })
        
        # Financial columns (20)
        columns.update({
            f'amount_{i+1}': 'currency' for i in range(10)
        })
        columns.update({
            f'profit_{i+1}': 'currency' for i in range(5)
        })
        columns.update({
            f'cost_{i+1}': 'currency' for i in range(5)
        })
        
        # Quantity columns (15)
        columns.update({
            f'quantity_{i+1}': 'quantity' for i in range(10)
        })
        columns.update({
            f'inventory_{i+1}': 'inventory' for i in range(5)
        })
        
        # Date columns (10)
        columns.update({
            'order_date': 'date',
            'ship_date': 'date',
            'delivery_date': 'date',
            'invoice_date': 'date',
            'payment_date': 'date',
            'last_contact': 'date',
            'created_date': 'date',
            'modified_date': 'date',
            'due_date': 'date',
            'closed_date': 'date'
        })
        
        # Status columns (15)
        columns.update({
            'order_status': 'status',
            'payment_status': 'status',
            'shipping_status': 'status',
            'quality_status': 'status',
            'approval_status': 'status'
        })
        columns.update({
            f'flag_{i+1}': 'boolean' for i in range(10)
        })
        
        # Score/Rating columns (10)
        columns.update({
            f'score_{i+1}': 'score' for i in range(5)
        })
        columns.update({
            f'rating_{i+1}': 'rating' for i in range(5)
        })
        
        # Text/Category columns (20)
        columns.update({
            'country': 'country',
            'state': 'state',
            'city': 'city',
            'product_name': 'product',
            'category_name': 'category',
            'brand_name': 'brand',
            'channel': 'channel',
            'source': 'source',
            'campaign': 'campaign',
            'segment': 'segment'
        })
        
        # Add attribute columns separately
        columns.update({
            f'attribute_{i+1}': 'attribute' for i in range(10)
        })
        
        return columns
    
    def _generate_chunk_data(self, rows: int, column_config: Dict, offset: int = 0) -> Dict:
        """⚙️ Generate data for a chunk"""
        
        data = {}
        
        # Set random seed for reproducible results
        np.random.seed(42 + offset)
        
        for col_name, col_type in column_config.items():
            
            if col_type == 'sequential_id':
                data[col_name] = range(offset + 1, offset + rows + 1)
                
            elif col_type == 'random_id':
                data[col_name] = np.random.randint(100000, 999999, rows)
                
            elif col_type == 'categorical':
                categories = [f'CAT_{i:03d}' for i in range(1, 51)]  # 50 categories
                data[col_name] = np.random.choice(categories, rows)
                
            elif col_type == 'currency':
                # Realistic business amounts
                data[col_name] = np.round(np.random.lognormal(6, 1.5, rows), 2)
                
            elif col_type == 'quantity':
                data[col_name] = np.random.randint(1, 1000, rows)
                
            elif col_type == 'inventory':
                data[col_name] = np.random.randint(0, 10000, rows)
                
            elif col_type == 'date':
                base_date = datetime(2020, 1, 1)
                days_range = (datetime.now() - base_date).days
                random_days = np.random.randint(0, days_range, rows)
                data[col_name] = [(base_date + timedelta(days=int(d))) for d in random_days]
                
            elif col_type == 'status':
                statuses = ['ACTIVE', 'PENDING', 'COMPLETED', 'CANCELLED', 'ON_HOLD']
                data[col_name] = np.random.choice(statuses, rows)
                
            elif col_type == 'boolean':
                data[col_name] = np.random.choice([True, False], rows)
                
            elif col_type == 'score':
                data[col_name] = np.round(np.random.uniform(0, 100, rows), 1)
                
            elif col_type == 'rating':
                data[col_name] = np.random.randint(1, 6, rows)  # 1-5 stars
                
            elif col_type == 'country':
                countries = ['USA', 'UK', 'Germany', 'France', 'Japan', 'India', 'China', 'Brazil']
                data[col_name] = np.random.choice(countries, rows)
                
            elif col_type == 'state':
                states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
                data[col_name] = np.random.choice(states, rows)
                
            elif col_type == 'city':
                cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                         'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
                data[col_name] = np.random.choice(cities, rows)
                
            elif col_type == 'product':
                products = [f'Product_{chr(65+i)}{j:03d}' for i in range(10) for j in range(1, 21)]
                data[col_name] = np.random.choice(products[:100], rows)
                
            elif col_type == 'category':
                categories = ['Electronics', 'Clothing', 'Home', 'Sports', 'Books', 
                             'Automotive', 'Health', 'Beauty', 'Toys', 'Food']
                data[col_name] = np.random.choice(categories, rows)
                
            elif col_type == 'brand':
                brands = [f'Brand_{chr(65+i)}' for i in range(20)]
                data[col_name] = np.random.choice(brands, rows)
                
            elif col_type == 'channel':
                channels = ['Online', 'Retail', 'Wholesale', 'Direct', 'Partner']
                data[col_name] = np.random.choice(channels, rows)
                
            elif col_type == 'source':
                sources = ['Website', 'Mobile', 'Phone', 'Email', 'Social', 'Referral']
                data[col_name] = np.random.choice(sources, rows)
                
            elif col_type == 'campaign':
                campaigns = [f'CAMP_{i:03d}' for i in range(1, 26)]
                data[col_name] = np.random.choice(campaigns, rows)
                
            elif col_type == 'segment':
                segments = ['Premium', 'Standard', 'Economy', 'Enterprise', 'SMB']
                data[col_name] = np.random.choice(segments, rows)
                
            elif col_type == 'attribute':
                attributes = [f'ATTR_{i}_{j}' for i in range(1, 6) for j in range(1, 11)]
                data[col_name] = np.random.choice(attributes[:20], rows)
        
        return data
    
    def generate_sample_conditions(self) -> List[str]:
        """📝 Generate sample filtering conditions for testing"""
        
        conditions = [
            # Financial conditions
            "(df['amount_1'] > 1000) & (df['profit_1'] > 100)",
            "(df['amount_2'] < 5000) | (df['cost_1'] > 500)",
            
            # Date conditions
            "df['order_date'] > '2023-01-01'",
            "(df['ship_date'] >= '2023-06-01') & (df['delivery_date'] <= '2024-01-01')",
            
            # Category conditions
            "df['country'].isin(['USA', 'UK', 'Germany'])",
            "(df['category_name'] == 'Electronics') & (df['brand_name'].str.startswith('Brand_A'))",
            
            # Quantity conditions
            "(df['quantity_1'] > 50) & (df['inventory_1'] < 1000)",
            "df['quantity_2'].between(10, 100)",
            
            # Status conditions
            "df['order_status'] == 'COMPLETED'",
            "(df['payment_status'] == 'ACTIVE') & (df['shipping_status'] != 'CANCELLED')",
            
            # Score conditions
            "(df['score_1'] > 80) & (df['rating_1'] >= 4)",
            "df['score_2'].between(60, 90)",
            
            # Complex multi-condition
            """(df['amount_1'] > 2000) & 
               (df['country'].isin(['USA', 'UK'])) & 
               (df['order_status'] == 'COMPLETED') & 
               (df['score_1'] > 75)""",
               
            # Boolean conditions
            "(df['flag_1'] == True) & (df['flag_2'] == False)",
            
            # Mixed conditions
            """(df['quantity_1'] > 100) & 
               ((df['profit_1'] > 200) | (df['score_1'] > 85)) &
               (df['category_name'].isin(['Electronics', 'Clothing']))"""
        ]
        
        return conditions


def generate_large_dataset():
    """🚀 Main function to generate large dataset"""
    
    print("🎯 LARGE DATASET GENERATOR")
    print("=" * 40)
    
    # Initialize generator
    generator = LargeDatasetGenerator(rows=1000000, columns=100)
    
    # Generate dataset
    csv_file = generator.generate_business_dataset("business_data_1M_100cols.csv")
    
    if csv_file:
        # Generate sample conditions
        conditions = generator.generate_sample_conditions()
        
        print(f"\n📋 Sample Filtering Conditions:")
        for i, condition in enumerate(conditions[:5], 1):
            print(f"   {i}. {condition}")
        
        print(f"\n💡 Use these files:")
        print(f"   • Dataset: {os.path.basename(csv_file)}")
        print(f"   • Conditions: See multiple_conditions_examples.py")
        
        return csv_file
    
    return None


if __name__ == "__main__":
    generate_large_dataset()