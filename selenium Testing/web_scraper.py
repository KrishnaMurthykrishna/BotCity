#!/usr/bin/env python3
"""
🕷️ The Internet Herokuapp Web Scraper
=====================================

Comprehensive web scraping script for https://the-internet.herokuapp.com/
Extracts and prints various data values from different pages and elements.

Scraping Targets:
- Available test scenarios/links
- Page titles and descriptions  
- Form data and input values
- Dynamic content and text
- Table data extraction
- List items and navigation elements
- Interactive element properties

Author: AI Assistant
Date: 2024-04-10
"""

from selenium_framework import SeleniumTestFramework
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json
from datetime import datetime


class InternetHerokuppScraper:
    """🕷️ Web scraper for The Internet Herokuapp"""
    
    def __init__(self, framework: SeleniumTestFramework):
        """
        Initialize the scraper
        
        Args:
            framework: SeleniumTestFramework instance
        """
        self.framework = framework
        self.base_url = "https://the-internet.herokuapp.com"
        self.scraped_data = {}
        
    def scrape_homepage_links(self):
        """🏠 Scrape all available test scenario links from homepage"""
        print("\n🏠 SCRAPING HOMEPAGE LINKS")
        print("=" * 40)
        
        if not self.framework.navigate_to(self.base_url):
            return
            
        try:
            # Get page title and heading
            page_title = self.framework.get_page_title()
            print(f"📄 Page Title: {page_title}")
            
            # Find main heading
            heading = self.framework.get_element_text(
                By.TAG_NAME, "h1", "Main heading"
            )
            print(f"🎯 Main Heading: {heading}")
            
            # Get all test scenario links
            links = self.framework.driver.find_elements(By.CSS_SELECTOR, "ul li a")
            
            test_scenarios = []
            for link in links:
                try:
                    link_text = link.text.strip()
                    link_href = link.get_attribute("href")
                    
                    if link_text and link_href:
                        test_scenarios.append({
                            'name': link_text,
                            'url': link_href,
                            'relative_path': link_href.replace(self.base_url, '')
                        })
                        print(f"🔗 {link_text} -> {link_href}")
                        
                except Exception as e:
                    continue
            
            self.scraped_data['homepage'] = {
                'title': page_title,
                'heading': heading,
                'available_scenarios': test_scenarios,
                'total_scenarios': len(test_scenarios)
            }
            
            print(f"\n✅ Found {len(test_scenarios)} test scenarios")
            
        except Exception as e:
            print(f"❌ Error scraping homepage: {str(e)}")
    
    def scrape_form_authentication_data(self):
        """🔐 Scrape form authentication page data"""
        print("\n🔐 SCRAPING FORM AUTHENTICATION PAGE")
        print("=" * 45)
        
        auth_url = f"{self.base_url}/login"
        if not self.framework.navigate_to(auth_url):
            return
            
        try:
            # Get page elements and their properties
            page_data = {
                'url': auth_url,
                'title': self.framework.get_page_title(),
                'heading': self.framework.get_element_text(By.TAG_NAME, "h2", "Page heading"),
                'form_elements': {}
            }
            
            # Username field data
            username_field = self.framework.find_element_safe(By.ID, "username")
            if username_field:
                page_data['form_elements']['username'] = {
                    'id': username_field.get_attribute("id"),
                    'name': username_field.get_attribute("name"),
                    'type': username_field.get_attribute("type"),
                    'placeholder': username_field.get_attribute("placeholder"),
                    'required': username_field.get_attribute("required"),
                    'current_value': username_field.get_attribute("value")
                }
                print(f"👤 Username Field: ID={username_field.get_attribute('id')}")
                print(f"   Type: {username_field.get_attribute('type')}")
                print(f"   Name: {username_field.get_attribute('name')}")
            
            # Password field data
            password_field = self.framework.find_element_safe(By.ID, "passwd")
            if password_field:
                page_data['form_elements']['password'] = {
                    'id': password_field.get_attribute("id"),
                    'name': password_field.get_attribute("name"), 
                    'type': password_field.get_attribute("type"),
                    'placeholder': password_field.get_attribute("placeholder")
                }
                print(f"🔒 Password Field: ID={password_field.get_attribute('id')}")
                print(f"   Type: {password_field.get_attribute('type')}")
            
            # Submit button data
            submit_button = self.framework.find_element_safe(By.CSS_SELECTOR, "button[type='submit']")
            if submit_button:
                page_data['form_elements']['submit_button'] = {
                    'type': submit_button.get_attribute("type"),
                    'text': submit_button.text,
                    'class': submit_button.get_attribute("class")
                }
                print(f"🔲 Submit Button: Text='{submit_button.text}'")
                print(f"   Class: {submit_button.get_attribute('class')}")
            
            # Get any instructional text
            content_div = self.framework.find_element_safe(By.ID, "content")
            if content_div:
                paragraphs = content_div.find_elements(By.TAG_NAME, "p")
                instructions = []
                for p in paragraphs:
                    if p.text.strip():
                        instructions.append(p.text.strip())
                        print(f"📝 Instruction: {p.text.strip()}")
                
                page_data['instructions'] = instructions
            
            self.scraped_data['form_authentication'] = page_data
            
        except Exception as e:
            print(f"❌ Error scraping form authentication: {str(e)}")
    
    def scrape_table_data(self):
        """📊 Scrape data from tables page"""
        print("\n📊 SCRAPING TABLE DATA")
        print("=" * 30)
        
        table_urls = [
            f"{self.base_url}/tables",
            f"{self.base_url}/challenging_dom"
        ]
        
        for url in table_urls:
            try:
                if not self.framework.navigate_to(url):
                    continue
                    
                page_name = url.split("/")[-1]
                print(f"\n🔍 Scraping: {page_name}")
                
                # Find all tables
                tables = self.framework.driver.find_elements(By.TAG_NAME, "table")
                
                table_data = []
                for i, table in enumerate(tables, 1):
                    print(f"\n📋 Table {i}:")
                    
                    # Get table headers
                    headers = []
                    header_elements = table.find_elements(By.TAG_NAME, "th")
                    for header in header_elements:
                        header_text = header.text.strip()
                        if header_text:
                            headers.append(header_text)
                    
                    print(f"   Headers: {headers}")
                    
                    # Get table rows
                    rows = []
                    row_elements = table.find_elements(By.TAG_NAME, "tr")
                    
                    for row_elem in row_elements[1:]:  # Skip header row
                        cells = row_elem.find_elements(By.TAG_NAME, "td")
                        row_data = []
                        for cell in cells:
                            cell_text = cell.text.strip()
                            row_data.append(cell_text)
                        
                        if row_data:
                            rows.append(row_data)
                            print(f"   Row: {row_data}")
                    
                    table_info = {
                        'headers': headers,
                        'rows': rows,
                        'row_count': len(rows),
                        'column_count': len(headers)
                    }
                    
                    table_data.append(table_info)
                
                self.scraped_data[f'tables_{page_name}'] = table_data
                print(f"\n✅ Found {len(table_data)} tables in {page_name}")
                
            except Exception as e:
                print(f"❌ Error scraping tables from {url}: {str(e)}")
    
    def scrape_dropdown_data(self):
        """📋 Scrape dropdown options and values"""
        print("\n📋 SCRAPING DROPDOWN DATA")
        print("=" * 35)
        
        dropdown_url = f"{self.base_url}/dropdown"
        if not self.framework.navigate_to(dropdown_url):
            return
            
        try:
            dropdown_element = self.framework.find_element_safe(By.ID, "dropdown")
            if dropdown_element:
                dropdown = Select(dropdown_element)
                
                # Get all options
                options = dropdown.options
                option_data = []
                
                print("📋 Dropdown Options:")
                for option in options:
                    option_info = {
                        'text': option.text,
                        'value': option.get_attribute('value'),
                        'selected': option.is_selected(),
                        'enabled': option.is_enabled()
                    }
                    option_data.append(option_info)
                    
                    status = "✅" if option.is_enabled() else "❌"
                    selected = "🔸" if option.is_selected() else "   "
                    print(f"   {status} {selected} '{option.text}' (value: '{option.get_attribute('value')}')")
                
                # Get currently selected option
                try:
                    selected_option = dropdown.first_selected_option
                    current_selection = {
                        'text': selected_option.text,
                        'value': selected_option.get_attribute('value')
                    }
                except:
                    current_selection = None
                
                self.scraped_data['dropdown'] = {
                    'options': option_data,
                    'total_options': len(option_data),
                    'current_selection': current_selection
                }
                
                print(f"\n✅ Found {len(option_data)} dropdown options")
                
        except Exception as e:
            print(f"❌ Error scraping dropdown: {str(e)}")
    
    def scrape_checkbox_data(self):
        """☑️ Scrape checkbox states and properties"""
        print("\n☑️ SCRAPING CHECKBOX DATA")
        print("=" * 35)
        
        checkbox_url = f"{self.base_url}/checkboxes"
        if not self.framework.navigate_to(checkbox_url):
            return
            
        try:
            checkboxes = self.framework.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            
            checkbox_data = []
            print("☑️ Checkbox States:")
            
            for i, checkbox in enumerate(checkboxes, 1):
                checkbox_info = {
                    'index': i,
                    'id': checkbox.get_attribute('id'),
                    'name': checkbox.get_attribute('name'),
                    'value': checkbox.get_attribute('value'),
                    'checked': checkbox.is_selected(),
                    'enabled': checkbox.is_enabled()
                }
                checkbox_data.append(checkbox_info)
                
                state = "☑️ CHECKED" if checkbox.is_selected() else "☐ UNCHECKED"
                enabled = "✅ Enabled" if checkbox.is_enabled() else "❌ Disabled"
                print(f"   Checkbox {i}: {state} | {enabled}")
                
                # Get any labels
                try:
                    label = checkbox.find_element(By.XPATH, "following-sibling::text()")
                    if label:
                        checkbox_info['label'] = label
                except:
                    pass
            
            self.scraped_data['checkboxes'] = checkbox_data
            print(f"\n✅ Found {len(checkbox_data)} checkboxes")
            
        except Exception as e:
            print(f"❌ Error scraping checkboxes: {str(e)}")
    
    def scrape_dynamic_content(self):
        """🔄 Scrape dynamic content and loading elements"""
        print("\n🔄 SCRAPING DYNAMIC CONTENT")
        print("=" * 40)
        
        dynamic_urls = [
            f"{self.base_url}/dynamic_content",
            f"{self.base_url}/dynamic_loading/1",
            f"{self.base_url}/dynamic_loading/2"
        ]
        
        for url in dynamic_urls:
            try:
                page_name = url.split("/")[-1]
                if page_name == "1" or page_name == "2":
                    page_name = f"dynamic_loading_{page_name}"
                    
                print(f"\n🔍 Scraping: {page_name}")
                
                if not self.framework.navigate_to(url):
                    continue
                
                page_data = {
                    'url': url,
                    'title': self.framework.get_page_title(),
                    'content': {}
                }
                
                if "dynamic_content" in url:
                    # Scrape dynamic content elements
                    content_rows = self.framework.driver.find_elements(By.CSS_SELECTOR, ".row")
                    
                    for i, row in enumerate(content_rows, 1):
                        try:
                            # Get image info
                            img = row.find_element(By.TAG_NAME, "img")
                            img_src = img.get_attribute("src") if img else None
                            
                            # Get text content
                            text_div = row.find_element(By.CSS_SELECTOR, ".large-10")
                            text_content = text_div.text.strip() if text_div else ""
                            
                            row_data = {
                                'image_src': img_src,
                                'text_content': text_content[:100] + "..." if len(text_content) > 100 else text_content
                            }
                            
                            page_data['content'][f'row_{i}'] = row_data
                            print(f"   Row {i}: {text_content[:50]}...")
                            
                        except Exception as e:
                            continue
                
                elif "dynamic_loading" in url:
                    # Get initial state
                    start_button = self.framework.find_element_safe(By.CSS_SELECTOR, "#start button")
                    if start_button:
                        page_data['content']['start_button'] = {
                            'text': start_button.text,
                            'visible': start_button.is_displayed(),
                            'enabled': start_button.is_enabled()
                        }
                        print(f"   Start Button: '{start_button.text}' (Visible: {start_button.is_displayed()})")
                    
                    # Check for loading indicator
                    loading_div = self.framework.find_element_safe(By.ID, "loading")
                    if loading_div:
                        page_data['content']['loading_indicator'] = {
                            'visible': loading_div.is_displayed(),
                            'text': loading_div.text
                        }
                        print(f"   Loading Indicator: Visible={loading_div.is_displayed()}")
                    
                    # Check for finish element (initially hidden)
                    finish_div = self.framework.find_element_safe(By.ID, "finish")
                    if finish_div:
                        page_data['content']['finish_element'] = {
                            'visible': finish_div.is_displayed(),
                            'text': finish_div.text if finish_div.is_displayed() else "Hidden"
                        }
                        print(f"   Finish Element: Visible={finish_div.is_displayed()}")
                
                self.scraped_data[page_name] = page_data
                
            except Exception as e:
                print(f"❌ Error scraping dynamic content from {url}: {str(e)}")
    
    def scrape_javascript_alert_info(self):
        """⚠️ Scrape JavaScript alerts page information"""
        print("\n⚠️ SCRAPING JAVASCRIPT ALERTS INFO")
        print("=" * 45)
        
        alerts_url = f"{self.base_url}/javascript_alerts"
        if not self.framework.navigate_to(alerts_url):
            return
            
        try:
            # Find alert buttons
            buttons = self.framework.driver.find_elements(By.TAG_NAME, "button")
            
            button_data = []
            print("⚠️ Alert Buttons Found:")
            
            for button in buttons:
                button_info = {
                    'text': button.text,
                    'onclick': button.get_attribute('onclick'),
                    'class': button.get_attribute('class'),
                    'enabled': button.is_enabled()
                }
                button_data.append(button_info)
                
                print(f"   🔲 '{button.text}' -> onclick: {button.get_attribute('onclick')}")
            
            # Get result paragraph
            result_p = self.framework.find_element_safe(By.ID, "result")
            result_text = result_p.text if result_p else "No result text"
            
            self.scraped_data['javascript_alerts'] = {
                'buttons': button_data,
                'result_element_text': result_text,
                'total_buttons': len(button_data)
            }
            
            print(f"\n✅ Found {len(button_data)} alert buttons")
            print(f"📄 Current result text: '{result_text}'")
            
        except Exception as e:
            print(f"❌ Error scraping JavaScript alerts: {str(e)}")
    
    def scrape_file_operations_info(self):
        """📁 Scrape file upload/download page information"""
        print("\n📁 SCRAPING FILE OPERATIONS INFO")
        print("=" * 45)
        
        file_urls = [
            f"{self.base_url}/upload",
            f"{self.base_url}/download"
        ]
        
        for url in file_urls:
            try:
                page_name = url.split("/")[-1]
                print(f"\n🔍 Scraping: {page_name} page")
                
                if not self.framework.navigate_to(url):
                    continue
                
                page_data = {
                    'url': url,
                    'title': self.framework.get_page_title(),
                    'elements': {}
                }
                
                if "upload" in url:
                    # File upload page
                    file_input = self.framework.find_element_safe(By.ID, "file-upload")
                    if file_input:
                        page_data['elements']['file_input'] = {
                            'id': file_input.get_attribute('id'),
                            'name': file_input.get_attribute('name'),
                            'type': file_input.get_attribute('type'),
                            'accept': file_input.get_attribute('accept')
                        }
                        print(f"   📎 File Input: ID={file_input.get_attribute('id')}")
                        print(f"      Accept: {file_input.get_attribute('accept')}")
                    
                    submit_button = self.framework.find_element_safe(By.ID, "file-submit")
                    if submit_button:
                        page_data['elements']['submit_button'] = {
                            'id': submit_button.get_attribute('id'),
                            'value': submit_button.get_attribute('value'),
                            'type': submit_button.get_attribute('type')
                        }
                        print(f"   🔲 Submit Button: Value='{submit_button.get_attribute('value')}'")
                
                elif "download" in url:
                    # File download page
                    download_links = self.framework.driver.find_elements(By.CSS_SELECTOR, "a[href*='.']")
                    
                    files_available = []
                    for link in download_links:
                        file_info = {
                            'text': link.text,
                            'href': link.get_attribute('href'),
                            'filename': link.get_attribute('href').split('/')[-1] if '/' in link.get_attribute('href') else link.text
                        }
                        files_available.append(file_info)
                        print(f"   📄 Available file: {link.text} -> {file_info['filename']}")
                    
                    page_data['elements']['available_files'] = files_available
                    page_data['elements']['file_count'] = len(files_available)
                
                self.scraped_data[f'file_{page_name}'] = page_data
                
            except Exception as e:
                print(f"❌ Error scraping file operations from {url}: {str(e)}")
    
    def print_scraped_summary(self):
        """📊 Print comprehensive summary of all scraped data"""
        print("\n" + "🕷️" * 20)
        print("🕷️" + " " * 15 + "SCRAPING SUMMARY" + " " * 15 + "🕷️")
        print("🕷️" * 20)
        
        total_items = 0
        
        for section, data in self.scraped_data.items():
            print(f"\n📋 {section.upper().replace('_', ' ')}")
            print("-" * 40)
            
            if section == 'homepage':
                print(f"   📄 Title: {data['title']}")
                print(f"   🎯 Heading: {data['heading']}")
                print(f"   🔗 Available Scenarios: {data['total_scenarios']}")
                total_items += data['total_scenarios']
                
            elif section == 'form_authentication':
                print(f"   📄 Title: {data['title']}")
                print(f"   📝 Form Elements: {len(data['form_elements'])}")
                print(f"   📋 Instructions: {len(data.get('instructions', []))}")
                total_items += len(data['form_elements'])
                
            elif 'tables' in section:
                table_count = len(data)
                total_rows = sum(table['row_count'] for table in data)
                print(f"   📊 Tables Found: {table_count}")
                print(f"   📋 Total Rows: {total_rows}")
                total_items += total_rows
                
            elif section == 'dropdown':
                print(f"   📋 Options Available: {data['total_options']}")
                if data['current_selection']:
                    print(f"   🔸 Current Selection: {data['current_selection']['text']}")
                total_items += data['total_options']
                
            elif section == 'checkboxes':
                checked_count = sum(1 for cb in data if cb['checked'])
                print(f"   ☑️ Total Checkboxes: {len(data)}")
                print(f"   ✅ Checked: {checked_count}")
                print(f"   ☐ Unchecked: {len(data) - checked_count}")
                total_items += len(data)
                
            elif section == 'javascript_alerts':
                print(f"   🔲 Alert Buttons: {data['total_buttons']}")
                print(f"   📄 Result Text: '{data['result_element_text']}'")
                total_items += data['total_buttons']
                
            elif 'dynamic' in section:
                content_items = len(data.get('content', {}))
                print(f"   🔄 Content Elements: {content_items}")
                total_items += content_items
                
            elif 'file' in section:
                elements_count = len(data.get('elements', {}))
                print(f"   📁 Page Elements: {elements_count}")
                total_items += elements_count
        
        # Overall statistics
        print("\n" + "=" * 50)
        print("📊 OVERALL SCRAPING STATISTICS")
        print("=" * 50)
        print(f"🌐 Website: {self.base_url}")
        print(f"🕷️ Sections Scraped: {len(self.scraped_data)}")
        print(f"📋 Total Data Items: {total_items}")
        print(f"⏰ Scraping Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Data size estimation
        import sys
        data_size = sys.getsizeof(str(self.scraped_data))
        print(f"💾 Data Size: ~{data_size} bytes")
        
        print("\n🎉 Web scraping completed successfully!")
        print("📄 All extracted data is available in scraped_data dictionary")
    
    def save_scraped_data(self, filename: str = None):
        """💾 Save scraped data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Scraped data saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving data: {str(e)}")
            return None
    
    def run_complete_scraping(self):
        """🚀 Execute complete scraping workflow"""
        print("🕷️ THE INTERNET HEROKUAPP - COMPREHENSIVE WEB SCRAPING")
        print("=" * 65)
        
        scraping_tasks = [
            ("🏠 Homepage Links", self.scrape_homepage_links),
            ("🔐 Form Authentication", self.scrape_form_authentication_data),
            ("📊 Table Data", self.scrape_table_data),
            ("📋 Dropdown Data", self.scrape_dropdown_data), 
            ("☑️ Checkbox Data", self.scrape_checkbox_data),
            ("🔄 Dynamic Content", self.scrape_dynamic_content),
            ("⚠️ JavaScript Alerts", self.scrape_javascript_alert_info),
            ("📁 File Operations", self.scrape_file_operations_info)
        ]
        
        for task_name, task_method in scraping_tasks:
            try:
                print(f"\n🔄 Starting: {task_name}")
                task_method()
                print(f"✅ Completed: {task_name}")
                
                # Brief pause between tasks
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error in {task_name}: {str(e)}")
                continue
        
        # Generate final report
        self.print_scraped_summary()
        
        # Save data to file
        saved_file = self.save_scraped_data()
        
        return self.scraped_data


def main():
    """🎯 Main scraper execution"""
    
    print("🕷️ Welcome to The Internet Herokuapp Web Scraper!")
    print("\nThis tool will extract and print various data from:")
    print("🌐 https://the-internet.herokuapp.com/")
    
    # Initialize Selenium framework
    framework = SeleniumTestFramework(
        browser="chrome",
        headless=False,  # Set to True for headless scraping
        implicit_wait=10
    )
    
    try:
        # Start browser
        print("\n🌐 Starting browser for web scraping...")
        framework.start_browser()
        
        # Initialize scraper
        scraper = InternetHerokuppScraper(framework)
        
        # Run complete scraping
        scraped_data = scraper.run_complete_scraping()
        
        # Take final screenshot
        framework.take_screenshot("scraping_completed")
        
        print(f"\n🎉 Scraping session completed successfully!")
        print(f"📊 Total sections scraped: {len(scraped_data)}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user")
        
    except Exception as e:
        print(f"\n❌ Scraping error: {str(e)}")
        framework.take_screenshot("scraping_error")
        
    finally:
        # Always cleanup
        print("\n🧹 Cleaning up browser...")
        framework.close_browser()
        print("✅ Scraping session ended")


if __name__ == "__main__":
    main()