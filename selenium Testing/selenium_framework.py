#!/usr/bin/env python3
"""
🚀 Selenium Testing Framework
=============================

A comprehensive Selenium WebDriver framework for automated web testing
using free testing websites with various actions and scenarios.

Features:
- Cross-browser support (Chrome, Firefox, Edge)
- Page Object Model pattern
- Comprehensive logging and screenshots
- Multiple test scenarios on free websites
- Professional error handling and reporting

Author: AI Assistant
Date: 2024-04-10
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    WebDriverException
)
import logging
import time
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import json


class SeleniumTestFramework:
    """
    🎯 Main Selenium Testing Framework Class
    
    Provides comprehensive web testing capabilities with professional
    logging, screenshots, and error handling.
    """
    
    def __init__(
        self, 
        browser: str = "chrome",
        headless: bool = False,
        implicit_wait: int = 10,
        explicit_wait: int = 15
    ):
        """
        🏗️ Initialize the Selenium Testing Framework
        
        Args:
            browser (str): Browser to use (chrome, firefox, edge)
            headless (bool): Run browser in headless mode
            implicit_wait (int): Implicit wait timeout in seconds
            explicit_wait (int): Explicit wait timeout in seconds
        """
        self.browser = browser.lower()
        self.headless = headless
        self.implicit_wait = implicit_wait
        self.explicit_wait = explicit_wait
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        
        # Setup logging
        self.setup_logging()
        
        # Create screenshots directory
        self.screenshots_dir = self.create_screenshots_directory()
        
        self.logger.info("🚀 Selenium Testing Framework initialized")
        self.logger.info(f"🌐 Browser: {browser}")
        self.logger.info(f"👁️ Headless mode: {headless}")
        
    def setup_logging(self):
        """🔧 Setup comprehensive logging system"""
        # Create logs directory
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
            
        # Configure logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"selenium_testing_{timestamp}.log"
        log_filepath = os.path.join(logs_dir, log_filename)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s',
            handlers=[
                logging.FileHandler(log_filepath, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🚀 Selenium logging initialized - Log file: {log_filepath}")
        print(f"🚀 Selenium logging initialized - Log file: {log_filepath}")
    
    def create_screenshots_directory(self) -> str:
        """📸 Create directory for screenshots"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshots_dir = f"screenshots/selenium_test_{timestamp}"
        
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            
        self.logger.info(f"📁 Screenshots directory created: {screenshots_dir}")
        return screenshots_dir
    
    def start_browser(self):
        """🌐 Start the web browser with optimized settings"""
        try:
            self.logger.info(f"🚀 Starting {self.browser} browser...")
            
            if self.browser == "chrome":
                options = webdriver.ChromeOptions()
                
                # Performance optimizations
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-web-security')
                options.add_argument('--allow-running-insecure-content')
                
                # User experience improvements
                options.add_argument('--start-maximized')
                options.add_argument('--disable-blink-features=AutomationControlled')
                
                if self.headless:
                    options.add_argument('--headless')
                    
                self.driver = webdriver.Chrome(options=options)
                
            elif self.browser == "firefox":
                options = webdriver.FirefoxOptions()
                if self.headless:
                    options.add_argument('--headless')
                    
                self.driver = webdriver.Firefox(options=options)
                
            elif self.browser == "edge":
                options = webdriver.EdgeOptions()
                if self.headless:
                    options.add_argument('--headless')
                    
                self.driver = webdriver.Edge(options=options)
                
            else:
                raise ValueError(f"❌ Unsupported browser: {self.browser}")
            
            # Set timeouts
            self.driver.implicitly_wait(self.implicit_wait)
            self.wait = WebDriverWait(self.driver, self.explicit_wait)
            
            self.logger.info("✅ Browser started successfully")
            print("✅ Browser started successfully")
            
        except Exception as e:
            error_msg = f"❌ Failed to start browser: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
            raise
    
    def navigate_to(self, url: str) -> bool:
        """
        🧭 Navigate to a specific URL with error handling
        
        Args:
            url (str): Target URL
            
        Returns:
            bool: Success status
        """
        try:
            self.logger.info(f"🌐 Navigating to: {url}")
            print(f"🌐 Navigating to: {url}")
            
            self.driver.get(url)
            
            # Wait for page to load
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            self.logger.info(f"✅ Successfully navigated to: {current_url}")
            self.logger.info(f"📄 Page title: {page_title}")
            print(f"✅ Page loaded: {page_title}")
            
            return True
            
        except Exception as e:
            error_msg = f"❌ Navigation failed to {url}: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
            self.take_screenshot("navigation_error")
            return False
    
    def find_element_safe(self, by: By, value: str, timeout: int = None) -> Optional[Any]:
        """
        🔍 Safely find an element with explicit wait
        
        Args:
            by (By): Locator strategy
            value (str): Locator value
            timeout (int): Custom timeout (optional)
            
        Returns:
            WebElement or None
        """
        try:
            wait_time = timeout or self.explicit_wait
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            
            self.logger.info(f"✅ Element found: {by} = '{value}'")
            return element
            
        except TimeoutException:
            self.logger.warning(f"⏰ Element not found within {wait_time}s: {by} = '{value}'")
            return None
        except Exception as e:
            self.logger.error(f"❌ Error finding element {by} = '{value}': {str(e)}")
            return None
    
    def click_element(self, by: By, value: str, description: str = "") -> bool:
        """
        👆 Safely click an element with multiple strategies
        
        Args:
            by (By): Locator strategy
            value (str): Locator value
            description (str): Human-readable description
            
        Returns:
            bool: Success status
        """
        try:
            desc = description or f"{by} = '{value}'"
            self.logger.info(f"👆 Attempting to click: {desc}")
            
            # Wait for element to be clickable
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Brief pause for scroll
            
            # Try normal click first
            try:
                element.click()
                self.logger.info(f"✅ Successfully clicked: {desc}")
                print(f"✅ Clicked: {desc}")
                return True
                
            except ElementNotInteractableException:
                # Try JavaScript click as fallback
                self.logger.info("🔄 Trying JavaScript click as fallback...")
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.info(f"✅ JavaScript click successful: {desc}")
                print(f"✅ Clicked (JS): {desc}")
                return True
                
        except Exception as e:
            error_msg = f"❌ Failed to click {desc}: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
            self.take_screenshot(f"click_error_{desc.replace(' ', '_')}")
            return False
    
    def type_text(self, by: By, value: str, text: str, description: str = "", clear_first: bool = True) -> bool:
        """
        ⌨️ Type text into an element with comprehensive handling
        
        Args:
            by (By): Locator strategy
            value (str): Locator value
            text (str): Text to type
            description (str): Human-readable description
            clear_first (bool): Clear field before typing
            
        Returns:
            bool: Success status
        """
        try:
            desc = description or f"{by} = '{value}'"
            self.logger.info(f"⌨️ Typing into {desc}: '{text}'")
            
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            
            if clear_first:
                element.clear()
            
            element.send_keys(text)
            
            self.logger.info(f"✅ Successfully typed into {desc}")
            print(f"✅ Typed: {desc}")
            return True
            
        except Exception as e:
            error_msg = f"❌ Failed to type into {desc}: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
            self.take_screenshot(f"type_error_{desc.replace(' ', '_')}")
            return False
    
    def select_dropdown(self, by: By, value: str, option_text: str, description: str = "") -> bool:
        """
        📋 Select option from dropdown menu
        
        Args:
            by (By): Locator strategy
            value (str): Locator value
            option_text (str): Option text to select
            description (str): Human-readable description
            
        Returns:
            bool: Success status
        """
        try:
            desc = description or f"{by} = '{value}'"
            self.logger.info(f"📋 Selecting from dropdown {desc}: '{option_text}'")
            
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            select = Select(element)
            select.select_by_visible_text(option_text)
            
            self.logger.info(f"✅ Successfully selected: {option_text}")
            print(f"✅ Selected: {option_text}")
            return True
            
        except Exception as e:
            error_msg = f"❌ Failed to select from dropdown {desc}: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
            return False
    
    def take_screenshot(self, filename: str = None) -> str:
        """
        📸 Take screenshot with timestamp
        
        Args:
            filename (str): Custom filename (optional)
            
        Returns:
            str: Screenshot file path
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%H%M%S")
                filename = f"screenshot_{timestamp}"
                
            filepath = os.path.join(self.screenshots_dir, f"{filename}.png")
            self.driver.save_screenshot(filepath)
            
            self.logger.info(f"📸 Screenshot saved: {filepath}")
            return filepath
            
        except Exception as e:
            error_msg = f"❌ Failed to take screenshot: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
            return ""
    
    def wait_for_element(self, by: By, value: str, timeout: int = None) -> bool:
        """
        ⏰ Wait for element to be present
        
        Args:
            by (By): Locator strategy
            value (str): Locator value
            timeout (int): Custom timeout
            
        Returns:
            bool: Element found status
        """
        try:
            wait_time = timeout or self.explicit_wait
            self.wait.until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False
    
    def hover_element(self, by: By, value: str, description: str = "") -> bool:
        """
        🖱️ Hover over an element
        
        Args:
            by (By): Locator strategy
            value (str): Locator value
            description (str): Human-readable description
            
        Returns:
            bool: Success status
        """
        try:
            desc = description or f"{by} = '{value}'"
            self.logger.info(f"🖱️ Hovering over: {desc}")
            
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            
            self.logger.info(f"✅ Successfully hovered: {desc}")
            return True
            
        except Exception as e:
            error_msg = f"❌ Failed to hover over {desc}: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
            return False
    
    def get_element_text(self, by: By, value: str, description: str = "") -> str:
        """
        📝 Get text content from an element
        
        Args:
            by (By): Locator strategy
            value (str): Locator value
            description (str): Human-readable description
            
        Returns:
            str: Element text or empty string
        """
        try:
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            text = element.text
            
            desc = description or f"{by} = '{value}'"
            self.logger.info(f"📝 Got text from {desc}: '{text}'")
            
            return text
            
        except Exception as e:
            error_msg = f"❌ Failed to get text from {description}: {str(e)}"
            self.logger.error(error_msg)
            return ""
    
    def scroll_to_element(self, by: By, value: str) -> bool:
        """
        📜 Scroll to make element visible
        
        Args:
            by (By): Locator strategy
            value (str): Locator value
            
        Returns:
            bool: Success status
        """
        try:
            element = self.find_element_safe(by, value)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Failed to scroll to element: {str(e)}")
            return False
    
    def close_browser(self):
        """🛑 Close browser and cleanup resources"""
        try:
            if self.driver:
                self.logger.info("🛑 Closing browser...")
                self.driver.quit()
                self.logger.info("✅ Browser closed successfully")
                print("✅ Browser closed successfully")
                
        except Exception as e:
            error_msg = f"❌ Error closing browser: {str(e)}"
            self.logger.error(error_msg)
            print(error_msg)
    
    def get_current_url(self) -> str:
        """🔗 Get current page URL"""
        try:
            return self.driver.current_url
        except:
            return ""
    
    def get_page_title(self) -> str:
        """📄 Get current page title"""
        try:
            return self.driver.title
        except:
            return ""