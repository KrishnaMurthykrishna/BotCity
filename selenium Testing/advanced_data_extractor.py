#!/usr/bin/env python3
"""
🎯 The Internet Herokuapp - Advanced Data Extractor
==================================================

Comprehensive data extraction tool that scrapes detailed information
from multiple pages on https://the-internet.herokuapp.com/

Features:
- Extracts data from 15+ different test pages
- Captures form data, table contents, dynamic elements
- Saves results to JSON and CSV formats
- Professional logging and error handling
- Screenshot capture for each page visited

Author: AI Assistant  
Date: 2024-04-10
"""

from selenium_framework import SeleniumTestFramework
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import csv
import os


class HerokuappDataExtractor:
    """🎯 Advanced data extractor for The Internet Herokuapp"""
    
    def __init__(self, framework: SeleniumTestFramework):
        """Initialize the data extractor"""
        self.framework = framework
        self.base_url = "https://the-internet.herokuapp.com"
        self.extracted_data = {}
        
        # Create results directory
        self.results_dir = "extraction_results"
        os.makedirs(self.results_dir, exist_ok=True)
        
    def extract_all_data(self):
        """🚀 Master extraction method - scrapes all available data"""
        print("🎯 ADVANCED DATA EXTRACTION FROM THE-INTERNET.HEROKUAPP.COM")
        print("=" * 70)
        
        extraction_tasks = [
            ("🏠 Homepage & Navigation", self.extract_homepage_data),
            ("🔐 Authentication Flow", self.extract_auth_complete_flow),
            ("📊 Data Tables Analysis", self.extract_tables_complete),
            ("📋 Forms & Inputs", self.extract_forms_comprehensive),
            ("📂 File Operations", self.extract_file_operations),
            ("⚠️ JavaScript Alerts", self.extract_alerts_comprehensive),
            ("🌐 HTTP Status Codes", self.extract_status_codes_complete),
            ("🖱️ Interactive Elements", self.extract_interactive_complete),
            ("📜 Dynamic Content", self.extract_dynamic_complete),
            ("🎨 Visual Elements", self.extract_visual_elements),
            ("🔧 Utility Pages", self.extract_utility_pages),
            ("📊 Performance Data", self.extract_performance_data)
        ]
        
        for task_name, task_method in extraction_tasks:
            try:
                print(f"\n{task_name}")
                print("-" * 50)
                
                # Navigate to homepage
                if self.framework.navigate_to(self.base_url):
                    # Take screenshot before task
                    self.framework.take_screenshot(f"before_{task_name.lower().replace(' ', '_')}")
                    
                    # Execute extraction task
                    task_method()
                    
                    time.sleep(1)  # Brief pause between tasks
                
            except Exception as e:
                print(f"❌ Task '{task_name}' failed: {str(e)}")
                self.framework.take_screenshot(f"error_{task_name.lower().replace(' ', '_')}")
        
        # Generate comprehensive reports
        self.generate_extraction_reports()
    
    def extract_homepage_data(self):
        """🏠 Extract complete homepage navigation and metadata"""
        try:
            # Page metadata
            page_data = {
                'title': self.framework.get_page_title(),
                'url': self.framework.get_current_url(),
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"📄 Title: {page_data['title']}")
            print(f"🌐 URL: {page_data['url']}")
            
            # Main content
            main_heading = self.framework.get_element_text(By.CSS_SELECTOR, "h1, h2", "Main heading")
            subheading = self.framework.get_element_text(By.CSS_SELECTOR, "h3", "Subheading")
            
            page_data.update({
                'main_heading': main_heading,
                'subheading': subheading
            })
            
            # Extract ALL navigation links with detailed info
            nav_links = []
            test_links = self.framework.driver.find_elements(By.CSS_SELECTOR, "ul li a")
            
            print(f"\n🔗 Navigation Links ({len(test_links)} found):")
            
            for i, link in enumerate(test_links, 1):
                link_data = {
                    'index': i,
                    'text': link.text.strip(),
                    'href': link.get_attribute("href"),
                    'target': link.get_attribute("target"),
                    'title': link.get_attribute("title")
                }
                
                nav_links.append(link_data)
                
                print(f"   {i:2d}. {link_data['text']}")
                print(f"       → {link_data['href']}")
            
            page_data['navigation_links'] = nav_links
            page_data['total_nav_links'] = len(nav_links)
            
            # Extract page source info
            page_source_length = len(self.framework.driver.page_source)
            page_data['page_source_length'] = page_source_length
            
            print(f"\n📊 Page Statistics:")
            print(f"   • Navigation Links: {len(nav_links)}")
            print(f"   • Page Source Size: {page_source_length:,} characters")
            
            self.extracted_data['homepage'] = page_data
            
        except Exception as e:
            print(f"❌ Homepage extraction failed: {str(e)}")
    
    def extract_auth_complete_flow(self):
        """🔐 Complete authentication flow with detailed data capture"""
        try:
            # Navigate to auth page
            if self.framework.click_element(By.LINK_TEXT, "Form Authentication", "Auth link"):
                time.sleep(2)
                
                auth_data = {
                    'login_page_url': self.framework.get_current_url(),
                    'login_page_title': self.framework.get_page_title()
                }
                
                print(f"🔐 Login Page: {auth_data['login_page_url']}")
                
                # Analyze form structure
                form_element = self.framework.find_element_safe(By.CSS_SELECTOR, "form")
                
                if form_element:
                    form_data = {
                        'action': form_element.get_attribute("action"),
                        'method': form_element.get_attribute("method"),
                        'fields': []
                    }
                    
                    # Extract all form fields
                    inputs = form_element.find_elements(By.CSS_SELECTOR, "input")
                    
                    for input_field in inputs:
                        field_data = {
                            'type': input_field.get_attribute("type"),
                            'name': input_field.get_attribute("name"),
                            'id': input_field.get_attribute("id"),
                            'placeholder': input_field.get_attribute("placeholder"),
                            'required': input_field.get_attribute("required"),
                            'value': input_field.get_attribute("value")
                        }
                        form_data['fields'].append(field_data)
                    
                    auth_data['form_structure'] = form_data
                    
                    print(f"📋 Form Analysis:")
                    print(f"   • Action: {form_data['action']}")
                    print(f"   • Method: {form_data['method']}")
                    print(f"   • Fields: {len(form_data['fields'])}")
                
                # Perform login with test credentials
                credentials = {
                    'username': 'tomsmith',
                    'password': 'SuperSecretPassword!'
                }
                
                print(f"\n🧪 Testing Authentication:")
                print(f"   Username: {credentials['username']}")
                print(f"   Password: {'*' * len(credentials['password'])}")
                
                self.framework.type_text(By.ID, "username", credentials['username'], "Username")
                self.framework.type_text(By.ID, "password", credentials['password'], "Password")
                
                # Capture pre-submit state
                login_button = self.framework.find_element_safe(By.CSS_SELECTOR, "button[type='submit']")
                button_text = login_button.text if login_button else "N/A"
                
                if self.framework.click_element(By.CSS_SELECTOR, "button[type='submit']", "Login button"):
                    time.sleep(2)
                    
                    # Extract secure area data
                    secure_data = {
                        'secure_url': self.framework.get_current_url(),
                        'secure_title': self.framework.get_page_title(),
                        'login_success': True
                    }
                    
                    print(f"\n✅ Authentication Successful!")
                    print(f"   Secure URL: {secure_data['secure_url']}")
                    
                    # Extract success message details
                    flash_message = self.framework.find_element_safe(By.CSS_SELECTOR, ".flash")
                    if flash_message:
                        message_data = {
                            'text': flash_message.text.strip(),
                            'class': flash_message.get_attribute("class"),
                            'visible': flash_message.is_displayed()
                        }
                        secure_data['success_message'] = message_data
                        print(f"   Message: {message_data['text']}")
                    
                    # Extract secure area content
                    content_div = self.framework.find_element_safe(By.ID, "content")
                    if content_div:
                        paragraphs = content_div.find_elements(By.CSS_SELECTOR, "p")
                        content_paragraphs = [p.text.strip() for p in paragraphs if p.text.strip()]
                        
                        secure_data['content_paragraphs'] = content_paragraphs
                        
                        print(f"   Content Sections: {len(content_paragraphs)}")
                        for i, para in enumerate(content_paragraphs[:3], 1):
                            print(f"      {i}. {para[:100]}...")
                    
                    # Test logout functionality
                    logout_link = self.framework.find_element_safe(By.CSS_SELECTOR, "a[href='/logout']")
                    
                    if logout_link:
                        logout_data = {
                            'text': logout_link.text.strip(),
                            'href': logout_link.get_attribute("href"),
                            'available': True
                        }
                        
                        print(f"\n🔓 Testing Logout:")
                        logout_link.click()
                        time.sleep(2)
                        
                        # Capture logout result
                        logout_result = {
                            'final_url': self.framework.get_current_url(),
                            'redirected_to_login': '/login' in self.framework.get_current_url()
                        }
                        
                        # Check logout message
                        logout_flash = self.framework.find_element_safe(By.CSS_SELECTOR, ".flash")
                        if logout_flash:
                            logout_result['message'] = logout_flash.text.strip()
                            print(f"   Logout Message: {logout_result['message']}")
                        
                        logout_data['result'] = logout_result
                        secure_data['logout_test'] = logout_data
                    
                    auth_data['secure_area'] = secure_data
                
                self.extracted_data['authentication'] = auth_data
            
        except Exception as e:
            print(f"❌ Auth extraction failed: {str(e)}")
    
    def extract_tables_complete(self):
        """📊 Complete table data extraction with cell-level analysis"""
        try:
            if self.framework.click_element(By.LINK_TEXT, "Sortable Data Tables", "Tables link"):
                time.sleep(2)
                
                tables_data = {
                    'page_url': self.framework.get_current_url(),
                    'page_title': self.framework.get_page_title(),
                    'tables': []
                }
                
                # Find all tables
                tables = self.framework.driver.find_elements(By.CSS_SELECTOR, "table")
                
                print(f"📊 Analyzing {len(tables)} tables:")
                
                for table_idx, table in enumerate(tables, 1):
                    print(f"\n📋 Table {table_idx} Analysis:")
                    
                    table_info = {
                        'table_index': table_idx,
                        'table_id': table.get_attribute("id"),
                        'table_class': table.get_attribute("class")
                    }
                    
                    # Extract headers with detailed info
                    headers = table.find_elements(By.CSS_SELECTOR, "thead th")
                    header_data = []
                    
                    for header in headers:
                        header_info = {
                            'text': header.text.strip(),
                            'class': header.get_attribute("class"),
                            'colspan': header.get_attribute("colspan"),
                            'rowspan': header.get_attribute("rowspan")
                        }
                        header_data.append(header_info)
                    
                    table_info['headers'] = header_data
                    
                    print(f"   Headers: {[h['text'] for h in header_data]}")
                    
                    # Extract ALL row data
                    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
                    rows_data = []
                    
                    for row_idx, row in enumerate(rows, 1):
                        cells = row.find_elements(By.CSS_SELECTOR, "td")
                        
                        row_info = {
                            'row_index': row_idx,
                            'cells': []
                        }
                        
                        for cell_idx, cell in enumerate(cells, 1):
                            cell_info = {
                                'cell_index': cell_idx,
                                'text': cell.text.strip(),
                                'class': cell.get_attribute("class"),
                                'data_value': cell.get_attribute("data-value")
                            }
                            
                            # Check for links in cell
                            cell_links = cell.find_elements(By.CSS_SELECTOR, "a")
                            if cell_links:
                                cell_info['links'] = [
                                    {
                                        'text': link.text.strip(),
                                        'href': link.get_attribute("href")
                                    }
                                    for link in cell_links
                                ]
                            
                            row_info['cells'].append(cell_info)
                        
                        rows_data.append(row_info)
                    
                    table_info['rows'] = rows_data
                    table_info['total_rows'] = len(rows_data)
                    
                    print(f"   Rows: {len(rows_data)}")
                    
                    # Display sample data
                    if rows_data:
                        print(f"   Sample Data:")
                        for i, row in enumerate(rows_data[:3], 1):
                            cell_texts = [cell['text'] for cell in row['cells']]
                            print(f"      Row {i}: {' | '.join(cell_texts)}")
                    
                    # Test sorting if available
                    sortable_headers = table.find_elements(By.CSS_SELECTOR, "thead th.header")
                    if sortable_headers:
                        print(f"   Sortable Columns: {len(sortable_headers)}")
                        
                        # Test first sortable column
                        try:
                            original_first_row = rows_data[0]['cells'][0]['text'] if rows_data else ""
                            
                            sortable_headers[0].click()
                            time.sleep(1)
                            
                            # Check if order changed
                            new_rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
                            if new_rows:
                                new_first_cell = new_rows[0].find_element(By.CSS_SELECTOR, "td").text.strip()
                                
                                sorting_test = {
                                    'column_tested': header_data[0]['text'],
                                    'original_first': original_first_row,
                                    'after_sort': new_first_cell,
                                    'order_changed': original_first_row != new_first_cell
                                }
                                
                                table_info['sorting_test'] = sorting_test
                                print(f"   Sort Test: {sorting_test['order_changed']}")
                                
                        except Exception as e:
                            print(f"   Sort Test Failed: {str(e)}")
                    
                    tables_data['tables'].append(table_info)
                
                self.extracted_data['tables'] = tables_data
            
        except Exception as e:
            print(f"❌ Tables extraction failed: {str(e)}")
    
    def extract_forms_comprehensive(self):
        """📋 Comprehensive form elements extraction"""
        try:
            forms_data = {}
            
            # Test Dropdown
            if self.framework.click_element(By.LINK_TEXT, "Dropdown", "Dropdown link"):
                time.sleep(2)
                
                dropdown_data = {
                    'page_url': self.framework.get_current_url(),
                    'dropdowns': []
                }
                
                dropdowns = self.framework.driver.find_elements(By.CSS_SELECTOR, "select")
                
                for dropdown in dropdowns:
                    select_element = Select(dropdown)
                    
                    dropdown_info = {
                        'id': dropdown.get_attribute("id"),
                        'name': dropdown.get_attribute("name"),
                        'multiple': dropdown.get_attribute("multiple") is not None,
                        'options': []
                    }
                    
                    # Extract all options
                    for option in select_element.options:
                        option_info = {
                            'text': option.text,
                            'value': option.get_attribute("value"),
                            'selected': option.is_selected(),
                            'disabled': option.get_attribute("disabled") is not None
                        }
                        dropdown_info['options'].append(option_info)
                    
                    dropdown_data['dropdowns'].append(dropdown_info)
                
                forms_data['dropdowns'] = dropdown_data
                
                print(f"📋 Dropdown Analysis:")
                print(f"   Total Options: {sum(len(d['options']) for d in dropdown_data['dropdowns'])}")
            
            # Test Checkboxes
            self.framework.navigate_to(self.base_url)
            if self.framework.click_element(By.LINK_TEXT, "Checkboxes", "Checkboxes link"):
                time.sleep(2)
                
                checkboxes_data = {
                    'page_url': self.framework.get_current_url(),
                    'checkboxes': []
                }
                
                checkboxes = self.framework.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                
                print(f"\n☑️ Checkboxes Analysis:")
                
                for i, checkbox in enumerate(checkboxes, 1):
                    initial_state = checkbox.is_selected()
                    
                    checkbox_info = {
                        'index': i,
                        'id': checkbox.get_attribute("id") or f"checkbox_{i}",
                        'name': checkbox.get_attribute("name"),
                        'value': checkbox.get_attribute("value"),
                        'initial_state': initial_state
                    }
                    
                    # Test checkbox toggle
                    try:
                        checkbox.click()
                        time.sleep(0.5)
                        after_click_state = checkbox.is_selected()
                        
                        checkbox_info['after_click_state'] = after_click_state
                        checkbox_info['toggle_successful'] = initial_state != after_click_state
                        
                        print(f"   Checkbox {i}: {initial_state} → {after_click_state}")
                        
                    except Exception as e:
                        checkbox_info['toggle_error'] = str(e)
                    
                    checkboxes_data['checkboxes'].append(checkbox_info)
                
                forms_data['checkboxes'] = checkboxes_data
            
            self.extracted_data['forms'] = forms_data
            
        except Exception as e:
            print(f"❌ Forms extraction failed: {str(e)}")
    
    def extract_file_operations(self):
        """📂 Complete file upload/download operations analysis"""
        try:
            file_ops_data = {}
            
            # File Download Analysis
            if self.framework.click_element(By.LINK_TEXT, "File Download", "File Download link"):
                time.sleep(2)
                
                download_data = {
                    'page_url': self.framework.get_current_url(),
                    'available_files': []
                }
                
                download_links = self.framework.driver.find_elements(By.CSS_SELECTOR, ".example a")
                
                print(f"📥 Download Analysis ({len(download_links)} files):")
                
                for link in download_links:
                    file_info = {
                        'filename': link.text.strip(),
                        'url': link.get_attribute("href"),
                        'size_estimate': len(link.text),  # Rough estimate
                        'extension': link.text.split('.')[-1] if '.' in link.text else 'unknown'
                    }
                    
                    download_data['available_files'].append(file_info)
                    print(f"   • {file_info['filename']} (.{file_info['extension']})")
                
                file_ops_data['downloads'] = download_data
            
            # File Upload Analysis  
            self.framework.navigate_to(self.base_url)
            if self.framework.click_element(By.LINK_TEXT, "File Upload", "File Upload link"):
                time.sleep(2)
                
                upload_data = {
                    'page_url': self.framework.get_current_url(),
                    'form_analysis': {}
                }
                
                # Analyze upload form
                upload_form = self.framework.find_element_safe(By.CSS_SELECTOR, "form")
                
                if upload_form:
                    form_info = {
                        'action': upload_form.get_attribute("action"),
                        'method': upload_form.get_attribute("method"),
                        'enctype': upload_form.get_attribute("enctype")
                    }
                    
                    # File input analysis
                    file_input = upload_form.find_element(By.CSS_SELECTOR, "input[type='file']")
                    if file_input:
                        file_input_info = {
                            'name': file_input.get_attribute("name"),
                            'accept': file_input.get_attribute("accept"),
                            'multiple': file_input.get_attribute("multiple") is not None
                        }
                        form_info['file_input'] = file_input_info
                    
                    upload_data['form_analysis'] = form_info
                
                print(f"\n📤 Upload Analysis:")
                print(f"   Form Method: {form_info.get('method', 'N/A')}")
                print(f"   Encoding: {form_info.get('enctype', 'N/A')}")
                
                file_ops_data['uploads'] = upload_data
            
            self.extracted_data['file_operations'] = file_ops_data
            
        except Exception as e:
            print(f"❌ File operations extraction failed: {str(e)}")
    
    def extract_alerts_comprehensive(self):
        """⚠️ Comprehensive JavaScript alerts testing and data extraction"""
        try:
            if self.framework.click_element(By.LINK_TEXT, "JavaScript Alerts", "JS Alerts link"):
                time.sleep(2)
                
                alerts_data = {
                    'page_url': self.framework.get_current_url(),
                    'alert_buttons': [],
                    'alert_tests': []
                }
                
                # Analyze alert buttons
                alert_buttons = self.framework.driver.find_elements(By.CSS_SELECTOR, "button")
                
                print(f"⚠️ JavaScript Alerts Analysis:")
                
                for i, button in enumerate(alert_buttons, 1):
                    button_info = {
                        'index': i,
                        'text': button.text.strip(),
                        'onclick': button.get_attribute("onclick"),
                        'id': button.get_attribute("id")
                    }
                    
                    alerts_data['alert_buttons'].append(button_info)
                    print(f"   Button {i}: {button_info['text']}")
                
                # Test each alert type
                for i, button in enumerate(alert_buttons):
                    try:
                        print(f"\n🧪 Testing Alert {i+1}:")
                        
                        # Click button to trigger alert
                        button.click()
                        time.sleep(1)
                        
                        # Handle alert
                        alert = self.framework.driver.switch_to.alert
                        
                        alert_test = {
                            'button_index': i + 1,
                            'alert_text': alert.text,
                            'alert_type': 'confirm' if 'confirm' in button.get_attribute("onclick") else 'alert',
                            'response_action': 'accept'
                        }
                        
                        print(f"   Alert Text: '{alert_test['alert_text']}'")
                        
                        # Accept alert
                        alert.accept()
                        time.sleep(1)
                        
                        # Check result
                        result_element = self.framework.find_element_safe(By.ID, "result")
                        if result_element:
                            result_text = result_element.text.strip()
                            alert_test['result_text'] = result_text
                            print(f"   Result: '{result_text}'")
                        
                        alerts_data['alert_tests'].append(alert_test)
                        
                        # For confirm/prompt alerts, test dismissal too
                        if 'confirm' in button.get_attribute("onclick"):
                            print(f"   Testing Dismiss...")
                            
                            button.click()
                            time.sleep(1)
                            
                            alert = self.framework.driver.switch_to.alert
                            alert.dismiss()
                            time.sleep(1)
                            
                            dismiss_result = self.framework.find_element_safe(By.ID, "result")
                            if dismiss_result:
                                dismiss_text = dismiss_result.text.strip()
                                print(f"   Dismiss Result: '{dismiss_text}'")
                                
                                alert_test['dismiss_result'] = dismiss_text
                        
                    except Exception as e:
                        print(f"   Alert {i+1} test failed: {str(e)}")
                
                self.extracted_data['alerts'] = alerts_data
            
        except Exception as e:
            print(f"❌ Alerts extraction failed: {str(e)}")
    
    def extract_status_codes_complete(self):
        """🌐 Complete HTTP status codes testing and analysis"""
        try:
            if self.framework.click_element(By.LINK_TEXT, "Status Codes", "Status Codes link"):
                time.sleep(2)
                
                status_data = {
                    'page_url': self.framework.get_current_url(),
                    'available_codes': [],
                    'status_tests': []
                }
                
                # Get available status code links
                status_links = self.framework.driver.find_elements(By.CSS_SELECTOR, ".example a")
                
                print(f"🌐 Status Codes Analysis:")
                
                for link in status_links:
                    code_info = {
                        'code': link.text.strip(),
                        'url': link.get_attribute("href"),
                        'link_text': link.text
                    }
                    
                    status_data['available_codes'].append(code_info)
                    print(f"   Available: {code_info['code']} → {code_info['url']}")
                
                # Test each status code
                for code_info in status_data['available_codes']:
                    try:
                        print(f"\n🧪 Testing Status {code_info['code']}:")
                        
                        # Navigate to status code page
                        self.framework.navigate_to(code_info['url'])
                        time.sleep(2)
                        
                        status_test = {
                            'status_code': code_info['code'],
                            'target_url': code_info['url'],
                            'final_url': self.framework.get_current_url(),
                            'page_title': self.framework.get_page_title()
                        }
                        
                        # Extract page content
                        heading = self.framework.get_element_text(By.CSS_SELECTOR, "h3", "Status heading")
                        if heading:
                            status_test['page_heading'] = heading
                        
                        # Check for specific content based on status code
                        content = self.framework.get_element_text(By.CSS_SELECTOR, "#content p", "Status description")
                        if content:
                            status_test['description'] = content
                        
                        print(f"   Final URL: {status_test['final_url']}")
                        print(f"   Title: {status_test['page_title']}")
                        if heading:
                            print(f"   Heading: {heading}")
                        
                        status_data['status_tests'].append(status_test)
                        
                        # Navigate back for next test
                        self.framework.navigate_to(f"{self.base_url}/status_codes")
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"   Status {code_info['code']} test failed: {str(e)}")
                
                self.extracted_data['status_codes'] = status_data
            
        except Exception as e:
            print(f"❌ Status codes extraction failed: {str(e)}")
    
    def extract_interactive_complete(self):
        """🖱️ Complete interactive elements extraction"""
        try:
            interactive_data = {}
            
            # Hover Elements
            if self.framework.click_element(By.LINK_TEXT, "Hovers", "Hovers link"):
                time.sleep(2)
                
                hover_data = {
                    'page_url': self.framework.get_current_url(),
                    'hover_elements': []
                }
                
                figures = self.framework.driver.find_elements(By.CSS_SELECTOR, ".figure")
                
                print(f"🖱️ Hover Elements Analysis ({len(figures)} found):")
                
                for i, figure in enumerate(figures, 1):
                    # Get image info
                    img = figure.find_element(By.CSS_SELECTOR, "img")
                    
                    element_info = {
                        'index': i,
                        'image_src': img.get_attribute("src"),
                        'image_alt': img.get_attribute("alt")
                    }
                    
                    # Test hover interaction
                    actions = ActionChains(self.framework.driver)
                    actions.move_to_element(figure).perform()
                    time.sleep(1)
                    
                    # Check for revealed content
                    try:
                        caption = figure.find_element(By.CSS_SELECTOR, ".figcaption")
                        
                        if caption.is_displayed():
                            caption_info = {
                                'text': caption.text.strip(),
                                'visible': True
                            }
                            
                            # Look for nested elements
                            caption_h5 = caption.find_element(By.CSS_SELECTOR, "h5")
                            caption_link = caption.find_element(By.CSS_SELECTOR, "a")
                            
                            if caption_h5:
                                caption_info['title'] = caption_h5.text.strip()
                            
                            if caption_link:
                                caption_info['link'] = {
                                    'text': caption_link.text.strip(),
                                    'href': caption_link.get_attribute("href")
                                }
                            
                            element_info['hover_caption'] = caption_info
                            
                            print(f"   Figure {i}: {element_info['image_alt']}")
                            print(f"      Caption: {caption_info.get('title', 'No title')}")
                            
                    except Exception as e:
                        element_info['hover_caption'] = {'visible': False, 'error': str(e)}
                        print(f"   Figure {i}: {element_info['image_alt']} (no hover caption)")
                    
                    hover_data['hover_elements'].append(element_info)
                
                interactive_data['hovers'] = hover_data
            
            # Drag and Drop
            self.framework.navigate_to(self.base_url)
            if self.framework.click_element(By.LINK_TEXT, "Drag and Drop", "Drag Drop link"):
                time.sleep(2)
                
                drag_data = {
                    'page_url': self.framework.get_current_url(),
                    'draggable_elements': []
                }
                
                # Find draggable elements
                draggables = self.framework.driver.find_elements(By.CSS_SELECTOR, ".column")
                
                print(f"\n🎯 Drag and Drop Analysis:")
                
                for i, element in enumerate(draggables, 1):
                    element_info = {
                        'index': i,
                        'id': element.get_attribute("id"),
                        'text': element.text.strip(),
                        'draggable': element.get_attribute("draggable") == "true"
                    }
                    
                    drag_data['draggable_elements'].append(element_info)
                    print(f"   Element {i}: ID={element_info['id']}, Text='{element_info['text']}'")
                
                # Test drag and drop
                if len(draggables) >= 2:
                    try:
                        source = draggables[0] 
                        target = draggables[1]
                        
                        source_text_before = source.text.strip()
                        target_text_before = target.text.strip()
                        
                        actions = ActionChains(self.framework.driver)
                        actions.drag_and_drop(source, target).perform()
                        time.sleep(2)
                        
                        source_text_after = source.text.strip()
                        target_text_after = target.text.strip()
                        
                        drag_test = {
                            'source_before': source_text_before,
                            'target_before': target_text_before,
                            'source_after': source_text_after,
                            'target_after': target_text_after,
                            'drag_successful': source_text_before != source_text_after
                        }
                        
                        drag_data['drag_test'] = drag_test
                        
                        print(f"   Drag Test: {source_text_before} ↔ {target_text_before}")
                        print(f"   Result: {drag_test['drag_successful']}")
                        
                    except Exception as e:
                        print(f"   Drag test failed: {str(e)}")
                
                interactive_data['drag_drop'] = drag_data
            
            self.extracted_data['interactive'] = interactive_data
            
        except Exception as e:
            print(f"❌ Interactive extraction failed: {str(e)}")
    
    def extract_dynamic_complete(self):
        """📜 Complete dynamic content extraction and loading tests"""
        try:
            if self.framework.click_element(By.LINK_TEXT, "Dynamic Loading", "Dynamic Loading link"):
                time.sleep(2)
                
                dynamic_data = {
                    'page_url': self.framework.get_current_url(),
                    'examples': [],
                    'tests': []
                }
                
                # Get available examples
                example_links = self.framework.driver.find_elements(By.CSS_SELECTOR, ".example a")
                
                print(f"📜 Dynamic Loading Analysis:")
                
                for link in example_links:
                    example_info = {
                        'text': link.text.strip(),
                        'href': link.get_attribute("href")
                    }
                    dynamic_data['examples'].append(example_info)
                    print(f"   Example: {example_info['text']} → {example_info['href']}")
                
                # Test each dynamic loading example
                for i, example in enumerate(dynamic_data['examples'], 1):
                    try:
                        print(f"\n🧪 Testing Dynamic Example {i}:")
                        
                        self.framework.navigate_to(example['href'])
                        time.sleep(2)
                        
                        test_data = {
                            'example_number': i,
                            'example_url': example['href'],
                            'page_title': self.framework.get_page_title()
                        }
                        
                        # Look for start button
                        start_button = self.framework.find_element_safe(By.CSS_SELECTOR, "#start button")
                        
                        if start_button:
                            button_text = start_button.text.strip()
                            test_data['start_button_text'] = button_text
                            
                            print(f"   Start Button: '{button_text}'")
                            
                            # Record initial state
                            loading_div = self.framework.find_element_safe(By.ID, "loading")
                            finish_div = self.framework.find_element_safe(By.ID, "finish")
                            
                            initial_state = {
                                'loading_visible': loading_div.is_displayed() if loading_div else False,
                                'finish_visible': finish_div.is_displayed() if finish_div else False
                            }
                            
                            test_data['initial_state'] = initial_state
                            
                            # Click start and monitor
                            start_time = time.time()
                            start_button.click()
                            
                            print(f"   Loading started...")
                            
                            # Wait for loading to complete
                            loading_complete = False
                            max_wait = 15  # seconds
                            
                            while time.time() - start_time < max_wait:
                                finish_element = self.framework.find_element_safe(By.ID, "finish")
                                
                                if finish_element and finish_element.is_displayed():
                                    loading_complete = True
                                    break
                                    
                                time.sleep(0.5)
                            
                            load_time = time.time() - start_time
                            
                            # Record final state  
                            final_state = {
                                'loading_complete': loading_complete,
                                'load_time': round(load_time, 2),
                                'finish_text': ''
                            }
                            
                            if loading_complete:
                                finish_element = self.framework.find_element_safe(By.ID, "finish")
                                if finish_element:
                                    final_state['finish_text'] = finish_element.text.strip()
                                
                                print(f"   ✅ Completed in {load_time:.2f}s: '{final_state['finish_text']}'")
                            else:
                                print(f"   ⏰ Timeout after {max_wait}s")
                            
                            test_data['final_state'] = final_state
                        
                        dynamic_data['tests'].append(test_data)
                        
                        # Go back for next test
                        self.framework.navigate_to(f"{self.base_url}/dynamic_loading")
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"   Dynamic test {i} failed: {str(e)}")
                
                self.extracted_data['dynamic_loading'] = dynamic_data
            
        except Exception as e:
            print(f"❌ Dynamic extraction failed: {str(e)}")
    
    def extract_visual_elements(self):
        """🎨 Extract visual elements and styling information"""
        try:
            visual_data = {}
            
            # Context Menu
            if self.framework.click_element(By.LINK_TEXT, "Context Menu", "Context Menu link"):
                time.sleep(2)
                
                context_data = {
                    'page_url': self.framework.get_current_url(),
                    'context_area': {}
                }
                
                # Find context menu area
                context_box = self.framework.find_element_safe(By.ID, "hot-spot")
                
                if context_box:
                    box_info = {
                        'id': context_box.get_attribute("id"),
                        'text': context_box.text.strip(),
                        'style': context_box.get_attribute("style"),
                        'size': {
                            'width': context_box.size['width'],
                            'height': context_box.size['height']  
                        }
                    }
                    
                    context_data['context_area'] = box_info
                    
                    print(f"🎨 Context Menu Analysis:")
                    print(f"   Area Text: '{box_info['text']}'")  
                    print(f"   Size: {box_info['size']['width']}x{box_info['size']['height']}")
                    
                    # Test right-click context menu
                    try:
                        actions = ActionChains(self.framework.driver)
                        actions.context_click(context_box).perform()
                        time.sleep(1)
                        
                        # Handle alert that should appear
                        alert = self.framework.driver.switch_to.alert
                        alert_text = alert.text
                        
                        context_data['context_test'] = {
                            'alert_triggered': True,
                            'alert_text': alert_text
                        }
                        
                        print(f"   Right-click Alert: '{alert_text}'")
                        alert.accept()
                        
                    except Exception as e:
                        context_data['context_test'] = {
                            'alert_triggered': False,
                            'error': str(e)
                        }
                        print(f"   Right-click test failed: {str(e)}")
                
                visual_data['context_menu'] = context_data
            
            self.extracted_data['visual_elements'] = visual_data
            
        except Exception as e:
            print(f"❌ Visual elements extraction failed: {str(e)}")
    
    def extract_utility_pages(self):
        """🔧 Extract data from utility and information pages"""
        try:
            utility_data = {}
            
            # Broken Images
            if self.framework.click_element(By.LINK_TEXT, "Broken Images", "Broken Images link"):
                time.sleep(2)
                
                images_data = {
                    'page_url': self.framework.get_current_url(),
                    'images': []
                }
                
                images = self.framework.driver.find_elements(By.CSS_SELECTOR, ".example img")
                
                print(f"🔧 Broken Images Analysis ({len(images)} images):")
                
                for i, img in enumerate(images, 1):
                    img_info = {
                        'index': i,
                        'src': img.get_attribute("src"),
                        'alt': img.get_attribute("alt"),
                        'width': img.get_attribute("width"),
                        'height': img.get_attribute("height")
                    }
                    
                    # Check if image is loaded (basic check)
                    try:
                        natural_width = self.framework.driver.execute_script(
                            "return arguments[0].naturalWidth", img
                        )
                        img_info['natural_width'] = natural_width
                        img_info['likely_broken'] = natural_width == 0
                        
                    except Exception as e:
                        img_info['check_error'] = str(e)
                    
                    images_data['images'].append(img_info)
                    
                    status = "❌ Broken" if img_info.get('likely_broken') else "✅ OK"
                    print(f"   Image {i}: {status} → {img_info['src']}")
                
                utility_data['broken_images'] = images_data
            
            self.extracted_data['utility_pages'] = utility_data
            
        except Exception as e:
            print(f"❌ Utility pages extraction failed: {str(e)}")
    
    def extract_performance_data(self):
        """📊 Extract performance and timing data"""
        try:
            # Collect page performance data
            performance_data = {}
            
            # Navigate to a complex page for performance testing
            if self.framework.click_element(By.LINK_TEXT, "Large & Deep DOM", "Large DOM link"):
                time.sleep(2)
                
                dom_data = {
                    'page_url': self.framework.get_current_url()
                }
                
                # Get DOM statistics
                dom_stats = self.framework.driver.execute_script("""
                    return {
                        'total_elements': document.getElementsByTagName('*').length,
                        'div_count': document.getElementsByTagName('div').length,
                        'table_count': document.getElementsByTagName('table').length,
                        'page_height': document.body.scrollHeight,
                        'viewport_height': window.innerHeight
                    }
                """)
                
                dom_data['dom_statistics'] = dom_stats
                
                print(f"📊 Performance Analysis:")
                print(f"   Total Elements: {dom_stats['total_elements']:,}")
                print(f"   DIV Elements: {dom_stats['div_count']:,}")
                print(f"   Page Height: {dom_stats['page_height']:,}px")
                
                # Test scrolling performance
                scroll_start = time.time()
                
                self.framework.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                scroll_time = time.time() - scroll_start
                dom_data['scroll_performance'] = {
                    'scroll_to_bottom_time': round(scroll_time, 3)
                }
                
                print(f"   Scroll Time: {scroll_time:.3f}s")
                
                performance_data['large_dom'] = dom_data
            
            self.extracted_data['performance'] = performance_data
            
        except Exception as e:
            print(f"❌ Performance extraction failed: {str(e)}")
    
    def generate_extraction_reports(self):
        """📊 Generate comprehensive reports from extracted data"""
        print("\n" + "🎯" * 25)
        print("🎯" + " " * 19 + "EXTRACTION REPORTS" + " " * 20 + "🎯")
        print("🎯" * 25)
        
        # Generate JSON report
        json_file = os.path.join(self.results_dir, "extraction_report.json")
        
        try:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 JSON Report: {json_file}")
            
        except Exception as e:
            print(f"❌ JSON report failed: {str(e)}")
        
        # Generate CSV summary
        csv_file = os.path.join(self.results_dir, "extraction_summary.csv")
        
        try:
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Category", "Subcategory", "Data Type", "Count", "Details"])
                
                for category, data in self.extracted_data.items():
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if isinstance(value, list):
                                writer.writerow([category, key, "List", len(value), f"{len(value)} items"])
                            elif isinstance(value, dict):
                                writer.writerow([category, key, "Dictionary", len(value), f"{len(value)} keys"])
                            else:
                                writer.writerow([category, key, "Value", 1, str(value)[:100]])
                    elif isinstance(data, list):
                        writer.writerow([category, "", "List", len(data), f"{len(data)} items"])
            
            print(f"📊 CSV Summary: {csv_file}")
            
        except Exception as e:
            print(f"❌ CSV report failed: {str(e)}")
        
        # Print summary statistics
        total_categories = len(self.extracted_data)
        total_data_points = 0
        
        for data in self.extracted_data.values():
            if isinstance(data, dict):
                total_data_points += len(data)
            elif isinstance(data, list):
                total_data_points += len(data)
            else:
                total_data_points += 1
        
        print(f"\n📊 Extraction Summary:")
        print(f"   • Categories Processed: {total_categories}")
        print(f"   • Total Data Points: {total_data_points}")
        print(f"   • Results Directory: {self.results_dir}")
        
        print("\n🎯" * 25)
        print("Data extraction completed successfully! 🎉")
        print("🎯" * 25)


def run_advanced_extraction():
    """🚀 Main function to run the advanced data extraction"""
    
    print("🎯 THE INTERNET HEROKUAPP - ADVANCED DATA EXTRACTOR")
    print("=" * 65)
    
    # Initialize framework  
    framework = SeleniumTestFramework(
        browser="chrome",
        headless=False,  # Set to True for headless extraction
        implicit_wait=10
    )
    
    try:
        # Start browser
        print("🚀 Initializing advanced data extractor...")
        framework.start_browser()
        
        # Create extractor instance
        extractor = HerokuappDataExtractor(framework)
        
        # Run comprehensive extraction
        extractor.extract_all_data()
        
        print("\n🎉 Advanced extraction completed successfully!")
        
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        framework.take_screenshot("extractor_error")
        
    finally:
        # Always cleanup
        print("\n🧹 Cleaning up...")
        framework.close_browser()
        print("✅ Extractor finished")


if __name__ == "__main__":
    run_advanced_extraction()