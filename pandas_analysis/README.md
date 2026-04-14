# 🎯 Pandas Analysis Suite
## Large Data • Multiple Conditions • Excel Pivots

Complete pandas data analysis suite for handling large datasets (10 lakh+ rows) with advanced filtering, multiple conditions, and professional Excel pivot table generation.

## 🚀 Features

### ✅ Large Dataset Generation
- **10 Lakh (1 million) rows** with 100 columns
- **Realistic business data** (sales, finance, inventory)
- **Multiple data types** (numeric, categorical, dates)
- **Memory-optimized** chunk processing
- **Progress tracking** and performance metrics

### ✅ Multiple Conditions Filtering
- **AND (&) conditions** with proper syntax
- **OR (|) conditions** and mixed logic
- **Complex nested conditions** with brackets
- **isin() method** for multiple values
- **between() method** for ranges  
- **query() method** for cleaner syntax
- **np.where() advanced usage** with multiple conditions
- **Negation (~)** and NOT conditions
- **Performance comparisons** between methods

### ✅ Excel Pivot Tables (win32com)
- **Automated pivot table creation** with display=True
- **Multiple pivot configurations** (sales, performance, time-based)
- **Professional formatting** and styling
- **Charts and visualizations** 
- **Executive dashboard** with KPIs
- **Real-time Excel display** for immediate viewing

### ✅ Performance Optimization
- **Chunk processing** for large files
- **Memory management** and cleanup
- **Speed benchmarking** across different methods
- **Efficient data types** and memory usage tracking

## 📁 Project Structure

```
pandas_analysis/
├── main_runner.py                    # 🎯 Main menu application
├── large_dataset_generator.py        # 🚀 Generate 10 lakh+ datasets  
├── multiple_conditions_examples.py   # 🎯 Advanced filtering demos
├── excel_pivot_creator.py            # 📊 Excel automation with win32com
├── requirements.txt                  # 📦 Dependencies
└── README.md                        # 📖 This documentation
```

## 🔧 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install pywin32 for Excel Integration
```bash
pip install pywin32
```

### 3. Verify Installation
```bash
python -c "import pandas, numpy, win32com.client; print('✅ All dependencies installed')"
```

## 🚀 Quick Start

### Option 1: Interactive Menu
```bash
python main_runner.py
```

### Option 2: Individual Components

#### Generate Large Dataset (10 Lakh rows)
```python
from large_dataset_generator import generate_large_dataset
csv_file = generate_large_dataset()
```

#### Test Multiple Conditions
```python  
from multiple_conditions_examples import run_conditions_demo
run_conditions_demo()
```

#### Create Excel Pivots
```python
from excel_pivot_creator import create_pivot_tables  
create_pivot_tables()  # Opens Excel with display=True
```

## 🎯 Multiple Conditions Examples

### 🔹 Basic AND Conditions
```python
# Financial filtering
df_filtered = df[(df['amount_1'] > 1000) & (df['amount_2'] < 5000)]

# Multiple criteria
df_filtered = df[
    (df['amount_1'] > 2000) & 
    (df['country'].isin(['USA', 'UK'])) & 
    (df['order_status'] == 'COMPLETED') & 
    (df['score_1'] > 75)
]
```

### 🔹 OR Conditions
```python
# Country filtering
df_filtered = df[(df['country'] == 'USA') | (df['country'] == 'UK')]
```

### 🔹 Mixed AND + OR (Brackets Important!)
```python
df_filtered = df[
    (df['amount_1'] > 500) & 
    ((df['country'] == 'USA') | (df['country'] == 'UK')) & 
    (df['status'] == 'ACTIVE')
]
```

### 🔹 Using .isin() for Multiple Values
```python
df_filtered = df[df['category'].isin(['Electronics', 'Clothing', 'Home'])]
```

### 🔹 Using .between() for Ranges
```python
df_filtered = df[df['amount'].between(1000, 5000)]
```

### 🔹 Using .query() (Cleaner Syntax)
```python
df_filtered = df.query('amount_1 > 1000 and country in ["USA", "UK"]')
```

### 🔹 Advanced np.where with Multiple Conditions
```python
df['category'] = np.where(
    (df['amount'] > 3000) & (df['score'] > 80),
    'High Value',
    np.where(
        (df['amount'] > 1000) & (df['score'] > 60),
        'Medium Value',
        'Standard'
    )
)
```

### 🔹 Negation (NOT ~)
```python
df_filtered = df[~((df['status'] == 'CANCELLED') | (df['amount'] < 100))]
```

### ⚠️ Common Mistakes to Avoid

❌ **Wrong:**
```python
df[df['col1'] > 500 and df['col2'] < 300]  # Python 'and', not pandas
```

✅ **Correct:**
```python  
df[(df['col1'] > 500) & (df['col2'] < 300)]  # Use & and brackets
```

## 📊 Dataset Schema

The generated business dataset includes:

### 📋 Core Identifiers (10 columns)
- `customer_id`, `order_id`, `product_id`, `region_id`
- `salesperson_id`, `store_id`, `supplier_id`

### 💰 Financial Data (20 columns)  
- `amount_1` to `amount_10` (revenue amounts)
- `profit_1` to `profit_5` (profit margins)
- `cost_1` to `cost_5` (cost data)

### 📦 Quantity Data (15 columns)
- `quantity_1` to `quantity_10` (order quantities)  
- `inventory_1` to `inventory_5` (stock levels)

### 📅 Date Fields (10 columns)
- `order_date`, `ship_date`, `delivery_date`
- `invoice_date`, `payment_date`, etc.

### 📊 Status & Flags (15 columns)
- `order_status` (ACTIVE, PENDING, COMPLETED, CANCELLED)
- `payment_status`, `shipping_status`
- `flag_1` to `flag_10` (boolean indicators)

### ⭐ Scores & Ratings (10 columns)
- `score_1` to `score_5` (0-100 performance scores)
- `rating_1` to `rating_5` (1-5 star ratings)

### 🌍 Geographic & Categories (20 columns)
- `country`, `state`, `city`
- `product_name`, `category_name`, `brand_name`
- `channel`, `source`, `campaign`, `segment`

## 📊 Excel Pivot Tables Features

### 🎯 Sales Analysis Pivot
- **Rows:** Country, Category  
- **Columns:** Year
- **Values:** Sum of Amount, Sum of Quantity
- **Professional formatting** and styling

### 🎯 Performance Analysis Pivot
- **Rows:** Order Status, Segment
- **Columns:** Country  
- **Values:** Average Amount, Average Score, Count of Orders

### 🎯 Time Analysis Pivot
- **Rows:** Year, Month (hierarchy)
- **Columns:** Category
- **Values:** Total Revenue, Total Profit

### 🎯 Advanced Analysis with Charts
- **Top 10 countries** by revenue
- **Automatic sorting** and filtering
- **Professional charts** and visualizations
- **Executive dashboard** with KPIs

## ⚡ Performance Benchmarks

### 📊 Typical Performance (10 lakh rows)
- **Data Generation:** ~30-60 seconds  
- **CSV Loading:** ~10-15 seconds (full dataset)
- **Simple Filtering:** ~0.1-0.5 seconds
- **Complex Conditions:** ~0.5-2 seconds
- **Excel Pivot Creation:** ~30-90 seconds

### 💾 Memory Usage
- **1M rows × 100 cols:** ~2-4 GB RAM
- **Optimized chunks:** 100K rows per chunk
- **Excel sample size:** 50K rows (for performance)

## 🎯 Menu Options

```
📋 MAIN MENU
1. 🚀 Generate Large Dataset (10 Lakh rows)
2. 🎯 Multiple Conditions Demo  
3. 📊 Excel Pivot Tables (win32com)
4. 🔄 Complete Workflow (All steps)
5. 📊 Performance Benchmark
6. 🔍 Dataset Information
0. 🚪 Exit
```

## 🛠️ Advanced Usage

### Custom Dataset Size
```python
from large_dataset_generator import LargeDatasetGenerator

# Custom configuration
generator = LargeDatasetGenerator(rows=2000000, columns=150) 
csv_file = generator.generate_business_dataset("custom_data.csv")
```

### Performance Testing
```python
from multiple_conditions_examples import PandasConditionsExpert

expert = PandasConditionsExpert("your_data.csv")
expert.run_all_demos(sample_size=500000)  # Test with 500K rows
```

### Headless Excel Processing
```python
from excel_pivot_creator import ExcelPivotCreator

creator = ExcelPivotCreator("your_data.csv")  
creator.create_comprehensive_pivot_analysis(display=False)  # No Excel UI
```

## 🚨 System Requirements

### 💻 Minimum Requirements
- **Python:** 3.8+
- **RAM:** 8+ GB (for 1M+ rows)
- **Storage:** 2+ GB free space
- **OS:** Windows (for win32com Excel integration)

### 🚀 Recommended Requirements  
- **Python:** 3.10+
- **RAM:** 16+ GB
- **Storage:** 5+ GB free space
- **CPU:** Multi-core for faster processing

## 🐛 Troubleshooting

### ❌ Common Issues

**1. Memory Error during data generation**
```python
# Solution: Use smaller chunks
generator = LargeDatasetGenerator(rows=500000, columns=50)
```

**2. win32com Excel errors**
```bash
# Solution: Reinstall pywin32
pip uninstall pywin32
pip install pywin32
python Scripts/pywin32_postinstall.py -install
```

**3. Pandas filtering syntax errors**
```python
# Wrong: df[df['col'] > 100 and df['col2'] < 200]
# Correct: df[(df['col'] > 100) & (df['col2'] < 200)]
```

### 🔍 Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Real Business Use Cases

### 🏪 Retail Analysis
```python  
# High-value customer analysis
high_value_customers = df[
    (df['amount_1'] > 5000) & 
    (df['order_status'] == 'COMPLETED') &
    (df['country'].isin(['USA', 'UK', 'Germany'])) &
    (df['score_1'] > 80)
]
```

### 📊 Finance Reporting
```python
# Quarterly profit analysis  
q4_profits = df[
    (df['order_quarter'] == 4) &
    (df['profit_1'] > 1000) &
    (df['category_name'].isin(['Electronics', 'Software']))
]
```

### 📦 Inventory Management
```python
# Low stock alerts
low_stock = df[
    (df['inventory_1'] < 100) &
    (df['category_name'] == 'Electronics') &
    (df['order_status'] == 'ACTIVE')
]
```

## 🎉 Success Metrics

After running the complete suite you'll have:

✅ **Generated:** 1M+ rows of realistic business data  
✅ **Learned:** 10+ advanced pandas filtering techniques  
✅ **Created:** Professional Excel pivot tables with charts  
✅ **Benchmarked:** Performance across different methods  
✅ **Mastered:** Large dataset handling and optimization  

## 🤝 Contributing

Want to extend the suite? Key areas for enhancement:

- **Additional data sources** (APIs, databases)
- **More pivot configurations** 
- **Advanced visualizations** 
- **Machine learning integration**
- **Web dashboard** (Streamlit/Dash)

## 📞 Support

For issues or questions:
1. Check the **troubleshooting section** above
2. Review **error messages** in the console
3. Verify **dependencies** are installed correctly
4. Test with **smaller datasets** first

---

**🎯 Ready to master pandas with large datasets and complex conditions?**

**Run `python main_runner.py` to get started!** 🚀