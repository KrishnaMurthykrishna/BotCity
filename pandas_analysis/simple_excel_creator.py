#!/usr/bin/env python3
"""
🎯 Simple Excel Creator - Quick Solution
========================================

Simple Excel workbook creator that bypasses complex pivot table creation
and focuses on creating a working Excel file with data and basic analysis.

Features:
- Load CSV data into Excel
- Create data tables 
- Add summary dashboard
- Display=True for immediate viewing
- Handles data type issues gracefully

"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

try:
    import win32com.client as win32
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("⚠️ win32com not available. Install with: pip install pywin32")


class SimpleExcelCreator:
    """🎯 Simple Excel workbook creator"""
    
    def __init__(self, csv_file: str):
        """Initialize with data source"""
        self.csv_file = csv_file
        self.excel_app = None
        self.workbook = None
        self.df = None
        
        if not WIN32_AVAILABLE:
            raise ImportError("win32com.client not available. Install pywin32.")
    
    def load_data(self) -> bool:
        """📂 Load CSV data"""
        try:
            print(f"📂 Loading data from {self.csv_file}...")
            
            self.df = pd.read_csv(self.csv_file)
            
            # Convert all data to simple types for Excel
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    # Convert to string to avoid issues
                    self.df[col] = self.df[col].astype(str)
            
            # Fill any missing values
            self.df = self.df.fillna('Unknown')
            
            print(f"✅ Data loaded: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load data: {str(e)}")
            return False
    
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
    
    def create_workbook_with_data(self) -> bool:
        """📊 Create workbook with data"""
        try:
            print(f"📊 Creating Excel workbook...")
            
            # Create new workbook
            self.workbook = self.excel_app.Workbooks.Add()
            
            # Create data sheet
            data_sheet = self.workbook.Worksheets(1)
            data_sheet.Name = "Raw Data"
            
            print(f"📝 Writing {len(self.df):,} rows to Excel...")
            
            # Write headers
            for col_idx, col_name in enumerate(self.df.columns, 1):
                data_sheet.Cells(1, col_idx).Value = str(col_name)
                data_sheet.Cells(1, col_idx).Font.Bold = True
            
            # Write data in smaller chunks to avoid memory issues
            chunk_size = 500
            total_written = 0
            
            for start_row in range(0, len(self.df), chunk_size):
                end_row = min(start_row + chunk_size, len(self.df))
                
                # Get chunk and convert to list of lists
                chunk_df = self.df.iloc[start_row:end_row]
                chunk_data = []
                
                for _, row in chunk_df.iterrows():
                    row_data = [str(val) if pd.notna(val) else "" for val in row.values]
                    chunk_data.append(row_data)
                
                # Write to Excel
                excel_start_row = start_row + 2  # +1 for header, +1 for 1-indexing
                excel_end_row = excel_start_row + len(chunk_data) - 1
                
                # Use A1 notation for range
                start_col = 'A'
                end_col = chr(ord('A') + len(self.df.columns) - 1)
                range_str = f"{start_col}{excel_start_row}:{end_col}{excel_end_row}"
                
                data_sheet.Range(range_str).Value = chunk_data
                
                total_written += len(chunk_data)
                if total_written % (chunk_size * 4) == 0:
                    print(f"   Progress: {total_written:,}/{len(self.df):,} rows")
            
            print(f"✅ Data written to Excel successfully")
            
            # Auto-fit columns
            data_sheet.Columns.AutoFit()
            
            # Create data table
            try:
                last_col = chr(ord('A') + len(self.df.columns) - 1)
                table_range = f"A1:{last_col}{len(self.df) + 1}"
                table = data_sheet.ListObjects.Add(1, data_sheet.Range(table_range), None, 1)
                table.Name = "DataTable"
                table.TableStyle = "TableStyleMedium2"
                print(f"✅ Data formatted as Excel table")
            except Exception as e:
                print(f"⚠️ Table formatting skipped: {str(e)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create workbook: {str(e)}")
            return False
    
    def create_summary_dashboard(self) -> bool:
        """📊 Create summary dashboard"""
        try:
            print(f"📊 Creating summary dashboard...")
            
            # Add new worksheet for dashboard
            dashboard_sheet = self.workbook.Worksheets.Add()
            dashboard_sheet.Name = "Dashboard"
            
            # Title
            dashboard_sheet.Cells(1, 1).Value = "🎯 DATA ANALYSIS DASHBOARD"
            dashboard_sheet.Cells(1, 1).Font.Size = 16
            dashboard_sheet.Cells(1, 1).Font.Bold = True
            dashboard_sheet.Range("A1:F1").Merge()
            
            row = 3
            
            # Basic stats
            dashboard_sheet.Cells(row, 1).Value = "📊 DATASET OVERVIEW"
            dashboard_sheet.Cells(row, 1).Font.Bold = True
            row += 1
            
            stats = [
                ("Total Records", f"{len(self.df):,}"),
                ("Total Columns", f"{len(self.df.columns)}"),
                ("Date Range", f"{datetime.now().strftime('%Y-%m-%d')}"),
            ]
            
            for label, value in stats:
                dashboard_sheet.Cells(row, 1).Value = label
                dashboard_sheet.Cells(row, 2).Value = value
                row += 1
            
            row += 1
            
            # Numeric analysis
            numeric_cols = [col for col in self.df.columns if col in ['amount', 'profit', 'score', 'quantity']]
            if numeric_cols:
                dashboard_sheet.Cells(row, 1).Value = "💰 NUMERIC ANALYSIS"
                dashboard_sheet.Cells(row, 1).Font.Bold = True
                row += 1
                
                for col in numeric_cols[:4]:  # Top 4 numeric columns
                    try:
                        col_data = pd.to_numeric(self.df[col], errors='coerce').dropna()
                        if len(col_data) > 0:
                            dashboard_sheet.Cells(row, 1).Value = f"{col.title()} Average"
                            dashboard_sheet.Cells(row, 2).Value = f"{col_data.mean():.2f}"
                            row += 1
                    except:
                        pass
            
            row += 1
            
            # Category analysis
            cat_cols = [col for col in self.df.columns if col in ['country', 'category', 'status']]
            if cat_cols:
                dashboard_sheet.Cells(row, 1).Value = "📋 CATEGORY ANALYSIS"
                dashboard_sheet.Cells(row, 1).Font.Bold = True
                row += 1
                
                for col in cat_cols[:3]:
                    try:
                        top_value = self.df[col].value_counts().index[0]
                        count = self.df[col].value_counts().iloc[0]
                        dashboard_sheet.Cells(row, 1).Value = f"Top {col.title()}"
                        dashboard_sheet.Cells(row, 2).Value = f"{top_value} ({count:,})"
                        row += 1
                    except:
                        pass
            
            # Format dashboard
            dashboard_sheet.Columns("A:B").AutoFit()
            
            print(f"✅ Dashboard created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create dashboard: {str(e)}")
            return False
    
    def save_workbook(self, filename: str = None) -> str:
        """💾 Save workbook"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"pandas_analysis_{timestamp}.xlsx"
            
            filepath = os.path.join(os.getcwd(), filename)
            self.workbook.SaveAs(filepath)
            
            print(f"💾 Workbook saved: {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Failed to save workbook: {str(e)}")
            return ""
    
    def close_excel(self):
        """🛑 Close Excel (optional - keep open for display=True)"""
        try:
            if self.excel_app:
                # Don't close - keep Excel open for user
                print(f"👁️ Excel remains open for viewing")
                # self.excel_app.Quit()
        except Exception as e:
            print(f"⚠️ Excel close warning: {str(e)}")


def main():
    """🎯 Main execution"""
    csv_file = "business_data_excel.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return
    
    try:
        print(f"🎯 SIMPLE EXCEL CREATOR")
        print(f"=" * 40)
        
        creator = SimpleExcelCreator(csv_file)
        
        # Load data
        if not creator.load_data():
            return
        
        # Start Excel
        if not creator.start_excel(display=True):
            return
        
        # Create workbook with data
        if not creator.create_workbook_with_data():
            return
        
        # Create dashboard  
        if not creator.create_summary_dashboard():
            return
        
        # Save workbook
        filepath = creator.save_workbook()
        
        if filepath:
            print(f"\n🎉 SUCCESS!")
            print(f"=" * 40)
            print(f"📄 Excel file: {os.path.basename(filepath)}")
            print(f"👁️ Excel is open with:")
            print(f"   • Raw Data sheet with {len(creator.df):,} rows")
            print(f"   • Dashboard with summary analysis")
            print(f"   • Display=True for immediate viewing")
            print(f"\n💡 You can now create pivot tables manually!")
            print(f"   Go to Insert → PivotTable in Excel")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()