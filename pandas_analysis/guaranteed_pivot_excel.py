#!/usr/bin/env python3
"""
Guaranteed Excel Pivot Data Creator
Creates Excel file with 50+ rows for pivot table analysis
"""

import pandas as pd
import win32com.client as win32
import numpy as np
import os
from datetime import datetime

def create_pivot_excel():
    print('🎯 GUARANTEED 50+ ROWS FOR PIVOT TABLES')
    print('=' * 50)

    # Simple, reliable dataset
    np.random.seed(99)
    rows = 50

    data = {
        'ID': list(range(1, rows + 1)),
        'Customer': [f'Cust_{i:03d}' for i in range(1, rows + 1)],
        'Amount': [round(100 + (i * 37.5), 2) for i in range(rows)],
        'Country': (['USA'] * 15 + ['UK'] * 15 + ['Germany'] * 20)[:rows],
        'Category': (['Electronics'] * 20 + ['Clothing'] * 30)[:rows], 
        'Status': (['Active'] * 30 + ['Completed'] * 20)[:rows],
        'Score': [round(50 + (i * 1.0), 1) for i in range(rows)],
        'Region': (['North'] * 25 + ['South'] * 25)[:rows]
    }

    df = pd.DataFrame(data)
    print(f'📊 Dataset: {len(df)} rows × {len(df.columns)} columns')

    # Start Excel
    excel = win32.Dispatch('Excel.Application')
    excel.Visible = True
    excel.DisplayAlerts = False
    print('✅ Excel started with Display=True')

    # Create workbook
    wb = excel.Workbooks.Add()
    ws = wb.Worksheets(1)
    ws.Name = 'PivotData'

    # Write headers
    headers = list(df.columns)
    for i, header in enumerate(headers, 1):
        ws.Cells(1, i).Value = header
        ws.Cells(1, i).Font.Bold = True

    print(f'📝 Writing {len(df)} data rows...')

    # Write data reliably
    data_written = 0
    for row in range(len(df)):
        for col in range(len(headers)):
            value = df.iloc[row, col]
            ws.Cells(row + 2, col + 1).Value = value
        
        data_written += 1
        if (row + 1) % 10 == 0:
            print(f'   ✅ {row + 1} rows written')

    # Save
    timestamp = datetime.now().strftime('%H%M%S')
    filename = f'pivot_ready_{timestamp}.xlsx'
    wb.SaveAs(os.path.join(os.getcwd(), filename))

    print(f'\n🎉 PERFECT SUCCESS!')
    print(f'=' * 35)
    print(f'📄 File: {filename}')
    print(f'📊 Data: {data_written} rows written ✅')
    print(f'📋 Headers: {len(headers)} columns')
    print('👁️ Excel open with complete data!')
    
    print(f'\n🎯 READY FOR PIVOT TABLES:')
    print(f'   • {data_written} rows of clean data')
    print('   • Multiple dimensions for analysis') 
    print('   • Go to Insert → PivotTable now!')

    print(f'\n📊 DATASET PREVIEW:')
    countries = sorted(df['Country'].unique())
    categories = sorted(df['Category'].unique())
    print(f'   • Countries: {countries}')
    print(f'   • Categories: {categories}')
    print(f'   • Amount range: ${df["Amount"].min()} - ${df["Amount"].max()}')
    print('   • Perfect for pivot analysis! 🎯')

if __name__ == "__main__":
    create_pivot_excel()