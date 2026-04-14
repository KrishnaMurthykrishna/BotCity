#!/usr/bin/env python3
"""
🎯 Excel Pivot Tables with win32com - Display True
=================================================

Creates professional Excel pivot tables from pandas data using win32com
with display=True for immediate visualization.

Features:
- Automatic Excel pivot table generation
- Multiple pivot configurations
- Professional formatting
- Charts and visualizations
- Display=True for immediate viewing
- Error handling and cleanup

Author: AI Assistant
Date: 2024-04-10
"""

import pandas as pd
import numpy as np
import os
import time
from datetime import datetime
import gc

try:
    import win32com.client as win32
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("⚠️ win32com not available. Install with: pip install pywin32")


class ExcelPivotCreator:
    """🎯 Professional Excel pivot table creator"""
    
    def __init__(self, csv_file: str):
        """Initialize with data source"""
        self.csv_file = csv_file
        self.excel_app = None
        self.workbook = None
        self.df = None
        
        if not WIN32_AVAILABLE:
            raise ImportError("win32com.client not available. Install pywin32.")
    
    def load_data(self, sample_size: int = 50000) -> bool:
        """📂 Load and prepare data for Excel"""
        try:
            print(f"📂 Loading data for Excel pivot tables...")
            
            # Load sample data for Excel (Excel handles smaller datasets better)
            total_lines = sum(1 for line in open(self.csv_file)) - 1
            if total_lines > sample_size:
                print(f"🎯 Sampling {sample_size:,} rows for Excel optimization...")
                skip_rows = sorted(np.random.choice(range(1, total_lines), 
                                                  total_lines - sample_size, 
                                                  replace=False))
                self.df = pd.read_csv(self.csv_file, skiprows=skip_rows)
            else:
                self.df = pd.read_csv(self.csv_file)
            
            # Data preprocessing for Excel
            self._prepare_data_for_excel()
            
            print(f"✅ Data loaded: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load data: {str(e)}")
            return False
    
    def _prepare_data_for_excel(self):
        """⚙️ Prepare data for Excel pivot tables"""
        
        # Convert dates to proper format
        date_columns = ['order_date', 'ship_date', 'delivery_date', 'invoice_date', 'payment_date']
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                
        # Add derived date fields for pivot analysis
        if 'order_date' in self.df.columns:
            self.df['order_year'] = self.df['order_date'].dt.year
            self.df['order_month'] = self.df['order_date'].dt.month
            self.df['order_quarter'] = self.df['order_date'].dt.quarter
            self.df['order_month_name'] = self.df['order_date'].dt.strftime('%B')
        
        # Clean up data types
        numeric_columns = [col for col in self.df.columns if 'amount' in col or 'profit' in col or 'cost' in col]
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
        
        # Handle missing values
        self.df = self.df.fillna('Unknown')
        
        print(f"🔧 Data prepared with {len(numeric_columns)} numeric columns")
    
    def start_excel(self, display: bool = True) -> bool:
        """🚀 Start Excel application"""
        try:
            print(f"🚀 Starting Excel application...")
            
            self.excel_app = win32.Dispatch("Excel.Application")
            self.excel_app.Visible = display
            self.excel_app.DisplayAlerts = False
            
            print(f"✅ Excel started (Display={display})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Excel: {str(e)}")
            return False
    
    def create_pivot_workbook(self) -> str:
        """📊 Create new workbook with data and pivot tables"""
        try:
            # Create new workbook
            self.workbook = self.excel_app.Workbooks.Add()
            
            # Write data to Excel
            worksheet = self.workbook.Worksheets(1)
            worksheet.Name = "Data"
            
            print(f"📝 Writing data to Excel...")
            
            # Write headers
            for col_idx, col_name in enumerate(self.df.columns, 1):
                worksheet.Cells(1, col_idx).Value = col_name
            
            # Write data in chunks for better performance
            chunk_size = 1000
            for start_row in range(0, len(self.df), chunk_size):
                end_row = min(start_row + chunk_size, len(self.df))
                
                # Convert chunk to list of lists
                chunk_data = self.df.iloc[start_row:end_row].values.tolist()
                
                # Write chunk to Excel
                start_excel_row = start_row + 2  # +2 for header and 1-indexing
                end_excel_row = end_row + 1
                
                range_str = f"A{start_excel_row}:{chr(64 + len(self.df.columns))}{end_excel_row}"
                worksheet.Range(range_str).Value = chunk_data
                
                if start_row % (chunk_size * 10) == 0:
                    print(f"   Progress: {end_row:,}/{len(self.df):,} rows")
            
            print(f"✅ Data written to Excel")
            
            # Format data as table
            data_range = f"A1:{chr(64 + len(self.df.columns))}{len(self.df) + 1}"
            table = worksheet.ListObjects.Add(1, worksheet.Range(data_range), None, 1)
            table.Name = "DataTable"
            table.TableStyle = "TableStyleMedium2"
            
            return "Data sheet created successfully"
            
        except Exception as e:
            print(f"❌ Failed to create workbook: {str(e)}")
            return ""
    
    def create_sales_pivot(self):
        """📊 Create Sales Analysis Pivot Table"""
        try:
            print(f"\n📊 Creating Sales Analysis pivot table...")
            
            # Add new worksheet for pivot
            pivot_sheet = self.workbook.Worksheets.Add()
            pivot_sheet.Name = "Sales Analysis"
            
            # Data source
            data_sheet = self.workbook.Worksheets("Data")
            data_range = data_sheet.UsedRange
            
            # Create pivot cache
            pivot_cache = self.workbook.PivotCaches().Create(1, data_range)
            
            # Create pivot table
            pivot_table = pivot_cache.CreatePivotTable(
                TableDestination=f"{pivot_sheet.Name}!R1C1",
                TableName="SalesAnalysisPivot"
            )
            
            # Configure pivot table fields
            # Row fields
            pivot_table.PivotFields("country").Orientation = 1  # xlRowField
            pivot_table.PivotFields("category_name").Orientation = 1
            
            # Column fields  
            if 'order_year' in self.df.columns:
                pivot_table.PivotFields("order_year").Orientation = 2  # xlColumnField
            
            # Data fields
            pivot_table.AddDataField(
                pivot_table.PivotFields("amount_1"), 
                "Sum of Amount", 
                -4157  # xlSum
            )
            
            pivot_table.AddDataField(
                pivot_table.PivotFields("quantity_1"), 
                "Sum of Quantity", 
                -4157
            )
            
            # Format pivot table
            pivot_table.TableStyle2 = "PivotStyleMedium9"
            pivot_table.ShowTableStyleRowStripes = True
            
            print(f"✅ Sales Analysis pivot created")
            
        except Exception as e:
            print(f"❌ Failed to create sales pivot: {str(e)}")
    
    def create_performance_pivot(self):
        """📊 Create Performance Analysis Pivot Table"""
        try:
            print(f"\n📊 Creating Performance Analysis pivot table...")
            
            # Add new worksheet
            pivot_sheet = self.workbook.Worksheets.Add()  
            pivot_sheet.Name = "Performance Analysis"
            
            # Data source
            data_sheet = self.workbook.Worksheets("Data")
            data_range = data_sheet.UsedRange
            
            # Create pivot cache
            pivot_cache = self.workbook.PivotCaches().Create(1, data_range)
            
            # Create pivot table
            pivot_table = pivot_cache.CreatePivotTable(
                TableDestination=f"{pivot_sheet.Name}!R1C1",
                TableName="PerformancePivot"
            )
            
            # Configure fields
            # Row fields
            pivot_table.PivotFields("order_status").Orientation = 1
            pivot_table.PivotFields("segment").Orientation = 1
            
            # Column fields
            pivot_table.PivotFields("country").Orientation = 2
            
            # Data fields
            pivot_table.AddDataField(
                pivot_table.PivotFields("amount_1"), 
                "Average Amount", 
                -4106  # xlAverage
            )
            
            pivot_table.AddDataField(
                pivot_table.PivotFields("score_1"), 
                "Average Score", 
                -4106
            )
            
            # Add count field
            pivot_table.AddDataField(
                pivot_table.PivotFields("customer_id"), 
                "Count of Orders", 
                -4112  # xlCount
            )
            
            # Format
            pivot_table.TableStyle2 = "PivotStyleMedium6"
            
            print(f"✅ Performance Analysis pivot created")
            
        except Exception as e:
            print(f"❌ Failed to create performance pivot: {str(e)}")
    
    def create_time_analysis_pivot(self):
        """📊 Create Time-based Analysis Pivot Table"""
        try:
            print(f"\n📊 Creating Time Analysis pivot table...")
            
            # Add new worksheet
            pivot_sheet = self.workbook.Worksheets.Add()
            pivot_sheet.Name = "Time Analysis"
            
            # Data source  
            data_sheet = self.workbook.Worksheets("Data")
            data_range = data_sheet.UsedRange
            
            # Create pivot cache
            pivot_cache = self.workbook.PivotCaches().Create(1, data_range)
            
            # Create pivot table
            pivot_table = pivot_cache.CreatePivotTable(
                TableDestination=f"{pivot_sheet.Name}!R1C1",
                TableName="TimeAnalysisPivot"
            )
            
            # Configure fields
            if 'order_year' in self.df.columns and 'order_month_name' in self.df.columns:
                # Row fields - Time hierarchy
                pivot_table.PivotFields("order_year").Orientation = 1
                pivot_table.PivotFields("order_month_name").Orientation = 1
                
                # Column fields
                pivot_table.PivotFields("category_name").Orientation = 2
                
                # Data fields
                pivot_table.AddDataField(
                    pivot_table.PivotFields("amount_1"), 
                    "Total Revenue", 
                    -4157  # xlSum
                )
                
                pivot_table.AddDataField(
                    pivot_table.PivotFields("profit_1"), 
                    "Total Profit", 
                    -4157
                )
                
                # Format
                pivot_table.TableStyle2 = "PivotStyleMedium12"
                
                print(f"✅ Time Analysis pivot created")
            else:
                print(f"⚠️ Time Analysis pivot skipped (date fields not available)")
            
        except Exception as e:
            print(f"❌ Failed to create time pivot: {str(e)}")
    
    def create_advanced_pivot_with_charts(self):
        """📊 Create Advanced Pivot with Charts"""
        try:
            print(f"\n📊 Creating Advanced Analysis with charts...")
            
            # Add new worksheet
            pivot_sheet = self.workbook.Worksheets.Add()
            pivot_sheet.Name = "Advanced Analysis"
            
            # Data source
            data_sheet = self.workbook.Worksheets("Data")
            data_range = data_sheet.UsedRange
            
            # Create pivot cache
            pivot_cache = self.workbook.PivotCaches().Create(1, data_range)
            
            # Create pivot table
            pivot_table = pivot_cache.CreatePivotTable(
                TableDestination=f"{pivot_sheet.Name}!R1C1",
                TableName="AdvancedPivot"
            )
            
            # Configure fields for TOP COUNTRIES analysis
            pivot_table.PivotFields("country").Orientation = 1
            
            # Data fields
            revenue_field = pivot_table.AddDataField(
                pivot_table.PivotFields("amount_1"), 
                "Total Revenue", 
                -4157  # xlSum
            )
            
            order_count_field = pivot_table.AddDataField(
                pivot_table.PivotFields("customer_id"), 
                "Order Count", 
                -4112  # xlCount
            )
            
            # Sort by revenue (descending)
            pivot_table.PivotFields("country").AutoSort(2, "Total Revenue")  # xlDescending
            
            # Show top 10 countries only
            pivot_table.PivotFields("country").PivotItems.Item(11).Visible = False
            
            # Format numbers
            revenue_field.NumberFormat = "$#,##0"
            order_count_field.NumberFormat = "#,##0"
            
            # Create chart
            chart_range = pivot_sheet.Range("A1:C12")  # Adjust range as needed
            chart = pivot_sheet.Shapes.AddChart2(240, 5).Chart  # xlColumnClustered
            chart.SetSourceData(chart_range)
            chart.ChartTitle.Text = "Revenue by Country"
            
            print(f"✅ Advanced Analysis with charts created")
            
        except Exception as e:
            print(f"❌ Failed to create advanced pivot: {str(e)}")
    
    def add_pivot_dashboard(self):
        """📊 Create Dashboard Summary"""
        try:
            print(f"\n📊 Creating Executive Dashboard...")
            
            # Add dashboard worksheet
            dashboard_sheet = self.workbook.Worksheets.Add()
            dashboard_sheet.Name = "Executive Dashboard"
            
            # Add title
            dashboard_sheet.Cells(1, 1).Value = "EXECUTIVE DASHBOARD"
            dashboard_sheet.Cells(1, 1).Font.Size = 18
            dashboard_sheet.Cells(1, 1).Font.Bold = True
            
            # Calculate summary metrics
            total_revenue = self.df['amount_1'].sum()
            total_orders = len(self.df)
            avg_order_value = self.df['amount_1'].mean()
            top_country = self.df['country'].value_counts().index[0]
            
            # Add KPIs
            kpis = [
                ("Total Revenue", f"${total_revenue:,.2f}"),
                ("Total Orders", f"{total_orders:,}"),
                ("Avg Order Value", f"${avg_order_value:.2f}"),
                ("Top Country", top_country),
            ]
            
            row = 3
            for metric, value in kpis:
                dashboard_sheet.Cells(row, 1).Value = metric
                dashboard_sheet.Cells(row, 2).Value = value
                dashboard_sheet.Cells(row, 1).Font.Bold = True
                row += 1
            
            # Format dashboard
            dashboard_sheet.Columns("A:B").AutoFit()
            
            print(f"✅ Executive Dashboard created")
            
        except Exception as e:
            print(f"❌ Failed to create dashboard: {str(e)}")
    
    def save_workbook(self, filename: str = None) -> str:
        """💾 Save workbook"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"pandas_pivot_analysis_{timestamp}.xlsx"
            
            filepath = os.path.join(os.getcwd(), filename)
            self.workbook.SaveAs(filepath)
            
            print(f"💾 Workbook saved: {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Failed to save workbook: {str(e)}")
            return ""
    
    def close_excel(self, save: bool = True):
        """🛑 Close Excel application"""
        try:
            if save and self.workbook:
                self.workbook.Save()
            
            if self.workbook:
                self.workbook.Close()
            
            if self.excel_app:
                self.excel_app.Quit()
            
            print(f"✅ Excel closed successfully")
            
        except Exception as e:
            print(f"⚠️ Error closing Excel: {str(e)}")
    
    def create_comprehensive_pivot_analysis(self, display: bool = True):
        """🚀 Create comprehensive pivot analysis"""
        
        print("🎯 EXCEL PIVOT TABLES CREATOR - COMPREHENSIVE ANALYSIS")
        print("=" * 65)
        
        try:
            # Load data
            if not self.load_data():
                return False
            
            # Start Excel
            if not self.start_excel(display=display):
                return False
            
            # Create workbook with data
            print(f"\n📊 Creating Excel workbook with pivot tables...")
            self.create_pivot_workbook()
            
            # Create multiple pivot tables
            pivot_tasks = [
                ("Sales Analysis", self.create_sales_pivot),
                ("Performance Analysis", self.create_performance_pivot),
                ("Time Analysis", self.create_time_analysis_pivot),
                ("Advanced Analysis", self.create_advanced_pivot_with_charts),
                ("Executive Dashboard", self.add_pivot_dashboard)
            ]
            
            for task_name, task_method in pivot_tasks:
                try:
                    task_method()
                    time.sleep(0.5)
                except Exception as e:
                    print(f"⚠️ {task_name} failed: {str(e)}")
            
            # Save workbook
            saved_file = self.save_workbook()
            
            if display:
                print(f"\n👁️ Excel is open with pivot tables (Display=True)")
                print(f"📊 Workbook contains multiple pivot analysis sheets")
                print(f"💾 File saved as: {os.path.basename(saved_file)}")
                
                # Keep Excel open for viewing
                input(f"\n👀 Review the pivot tables in Excel, then press Enter to close...")
                
            # Close Excel
            self.close_excel(save=True)
            
            return True
            
        except Exception as e:
            print(f"❌ Pivot analysis failed: {str(e)}")
            self.close_excel(save=False)
            return False


def create_pivot_tables():
    """🚀 Main function to create pivot tables"""
    
    if not WIN32_AVAILABLE:
        print("❌ win32com not available. Install with: pip install pywin32")
        return
    
    # Check for data file
    csv_file = "business_data_1M_100cols.csv"
    
    if not os.path.exists(csv_file):
        print("📂 Large dataset not found. Creating sample dataset...")
        
        # Create smaller sample for Excel demo
        from large_dataset_generator import LargeDatasetGenerator
        generator = LargeDatasetGenerator(rows=50000, columns=50)  # Smaller for Excel
        csv_file = generator.generate_business_dataset("sample_business_data.csv")
        
        if not csv_file:
            print("❌ Failed to generate sample dataset")
            return
    
    # Create pivot tables
    creator = ExcelPivotCreator(csv_file)
    success = creator.create_comprehensive_pivot_analysis(display=True)
    
    if success:
        print(f"\n🎉 Pivot table analysis completed successfully!")
        print(f"📊 Multiple pivot tables created with professional formatting")
        print(f"📈 Charts and dashboard included")
    else:
        print(f"\n❌ Pivot table creation failed")


if __name__ == "__main__":
    create_pivot_tables()