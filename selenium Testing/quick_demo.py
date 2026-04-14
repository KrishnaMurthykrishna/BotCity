#!/usr/bin/env python3
"""
🎯 Quick Demo Test
==================

A simple demonstration of the Selenium Testing Framework
showing basic functionality and how to create custom tests.

This demo performs:
1. Browser initialization  
2. Navigation to a test site
3. Basic element interactions
4. Screenshot capture
5. Proper cleanup

Perfect for understanding the framework before running full test suites.

Author: AI Assistant
Date: 2024-04-10
"""

from selenium_framework import SeleniumTestFramework
from selenium.webdriver.common.by import By
import time


def run_quick_demo():
    """🚀 Simple demonstration of Selenium framework capabilities"""
    
    print("🎯 SELENIUM TESTING FRAMEWORK - QUICK DEMO")
    print("=" * 50)
    
    # Initialize framework
    framework = SeleniumTestFramework(
        browser="chrome",
        headless=False,  # Set to True for headless mode
        implicit_wait=10
    )
    
    try:
        # Start browser
        print("🌐 Starting browser...")
        framework.start_browser()
        
        # Navigate to test site
        print("🔗 Navigating to test website...")
        if framework.navigate_to("https://the-internet.herokuapp.com"):
            
            # Take initial screenshot
            framework.take_screenshot("demo_homepage")
            
            # Test basic page interaction
            print("🔍 Testing basic interactions...")
            
            # Click on form authentication link
            if framework.click_element(
                By.LINK_TEXT, "Form Authentication",
                "Form Authentication link"  
            ):
                
                # Fill username
                if framework.type_text(
                    By.ID, "username", 
                    "tomsmith", 
                    "Username field"
                ):
                    print("✅ Username entered successfully")
                
                # Fill password  
                if framework.type_text(
                    By.ID, "password",
                    "SuperSecretPassword!",
                    "Password field"
                ):
                    print("✅ Password entered successfully")
                
                # Take screenshot before login
                framework.take_screenshot("demo_before_login")
                
                # Click login button
                if framework.click_element(
                    By.CSS_SELECTOR, "button[type='submit']",
                    "Login button"
                ):
                    
                    # Wait for page to load
                    time.sleep(2)
                    
                    # Check for success message
                    success_msg = framework.get_element_text(
                        By.CSS_SELECTOR, ".flash.success",
                        "Success message"
                    )
                    
                    if success_msg:
                        print(f"✅ Login successful: {success_msg}")
                        
                        # 🔍 SCRAPE AND PRINT DETAILED PAGE INFORMATION
                        print("\n" + "="*60)
                        print("📊 DETAILED PAGE INFORMATION AFTER LOGIN")
                        print("="*60)
                        
                        # 1. Get current page details
                        current_url = framework.get_current_url()
                        page_title = framework.get_page_title()
                        print(f"🌐 Current URL: {current_url}")
                        print(f"📄 Page Title: {page_title}")
                        
                        # 2. Get main heading
                        main_heading = framework.get_element_text(
                            By.CSS_SELECTOR, "h2",
                            "Main heading"
                        )
                        if main_heading:
                            print(f"📋 Main Heading: {main_heading}")
                        
                        # 3. Get all text content from the secure area
                        secure_content = framework.get_element_text(
                            By.CSS_SELECTOR, "#content",
                            "Secure area content"
                        )
                        if secure_content:
                            print(f"📝 Secure Area Content:")
                            # Clean up the content and print key parts
                            lines = [line.strip() for line in secure_content.split('\n') if line.strip()]
                            for line in lines:
                                if line and len(line) > 1:
                                    print(f"   • {line}")
                        
                        # 4. Find and print available links
                        try:
                            links = framework.driver.find_elements(By.CSS_SELECTOR, "a")
                            if links:
                                print(f"\n🔗 Available Links on Secure Page:")
                                for i, link in enumerate(links, 1):
                                    link_text = link.text.strip()
                                    link_href = link.get_attribute("href")
                                    if link_text:
                                        print(f"   {i}. '{link_text}' → {link_href}")
                        except Exception as e:
                            print(f"⚠️ Could not extract links: {str(e)}")
                        
                        # 5. Check for any other elements with text
                        try:
                            # Get all paragraphs
                            paragraphs = framework.driver.find_elements(By.CSS_SELECTOR, "p")
                            if paragraphs:
                                print(f"\n📄 Paragraphs Found:")
                                for i, p in enumerate(paragraphs, 1):
                                    p_text = p.text.strip()
                                    if p_text:
                                        print(f"   P{i}: {p_text}")
                        except:
                            pass
                        
                        # 6. Check for any buttons
                        try:
                            buttons = framework.driver.find_elements(By.CSS_SELECTOR, "button, input[type='button'], input[type='submit']")
                            if buttons:
                                print(f"\n🔲 Buttons Found:")
                                for i, button in enumerate(buttons, 1):
                                    button_text = button.text.strip() or button.get_attribute("value") or button.get_attribute("id")
                                    if button_text:
                                        print(f"   Button{i}: {button_text}")
                        except:
                            pass
                        
                        # 7. Get page source length and other metrics
                        try:
                            page_source_length = len(framework.driver.page_source)
                            print(f"\n📊 Page Statistics:")
                            print(f"   📏 Page Source Length: {page_source_length:,} characters")
                            print(f"   🕒 Current Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                        except:
                            pass
                        
                        # 8. Test logout functionality and print result
                        print(f"\n🔓 Testing Logout Functionality:")
                        logout_link = framework.find_element_safe(By.CSS_SELECTOR, "a[href='/logout']")
                        if logout_link:
                            logout_text = logout_link.text
                            logout_href = logout_link.get_attribute("href")
                            print(f"   🔗 Logout Link Found: '{logout_text}' → {logout_href}")
                            
                            # Click logout and verify
                            logout_link.click()
                            time.sleep(2)
                            
                            # Check if logout was successful
                            logout_success = framework.get_element_text(
                                By.CSS_SELECTOR, ".flash",
                                "Logout message"
                            )
                            
                            if logout_success:
                                print(f"   ✅ Logout Result: {logout_success}")
                                
                            # Get final page info after logout
                            final_url = framework.get_current_url() 
                            final_title = framework.get_page_title()
                            print(f"   🌐 After Logout URL: {final_url}")
                            print(f"   📄 After Logout Title: {final_title}")
                        else:
                            print("   ⚠️ Logout link not found")
                        
                        print("="*60)
                    
                    # Take final screenshot
                    framework.take_screenshot("demo_login_success")
            
            # Navigate back to homepage  
            print("🏠 Returning to homepage...")
            framework.navigate_to("https://the-internet.herokuapp.com")
            
            # Test another element - checkboxes
            print("☑️ Testing checkbox interactions...")
            if framework.click_element(
                By.LINK_TEXT, "Checkboxes",
                "Checkboxes link"
            ):
                
                # Find checkboxes and toggle them
                checkboxes = framework.driver.find_elements(
                    By.CSS_SELECTOR, "input[type='checkbox']"
                )
                
                for i, checkbox in enumerate(checkboxes, 1):
                    initial_state = checkbox.is_selected()
                    checkbox.click()
                    new_state = checkbox.is_selected()
                    
                    print(f"✅ Checkbox {i}: {initial_state} → {new_state}")
                
                framework.take_screenshot("demo_checkboxes")
            
            # Demo complete
            print("\n🎉 Demo completed successfully!")
            print("📸 Screenshots saved to screenshots/ directory")
            print("📝 Logs available in logs/ directory")
            
        else:
            print("❌ Failed to navigate to test website")
            
    except Exception as e:
        print(f"❌ Demo encountered an error: {str(e)}")
        framework.take_screenshot("demo_error")
        
    finally:
        # Always cleanup
        print("🧹 Cleaning up...")
        framework.close_browser()
        print("✅ Demo finished")


def run_mini_test_suite():
    """🧪 Mini test suite showing multiple website interactions"""
    
    print("\n🧪 MINI TEST SUITE DEMO")
    print("=" * 40)
    
    framework = SeleniumTestFramework(browser="chrome", headless=False)
    
    test_sites = [
        {
            'name': 'The Internet - Dynamic Loading',
            'url': 'https://the-internet.herokuapp.com/dynamic_loading/1',
            'action': 'Click Start button and wait for content'
        },
        {
            'name': 'The Internet - Hover',  
            'url': 'https://the-internet.herokuapp.com/hovers',
            'action': 'Hover over images to reveal captions'
        }
    ]
    
    try:
        framework.start_browser()
        
        for i, site in enumerate(test_sites, 1):
            print(f"\n🌐 Test {i}: {site['name']}")
            print(f"📋 Action: {site['action']}")
            
            if framework.navigate_to(site['url']):
                
                if 'dynamic_loading' in site['url']:
                    # Test dynamic loading
                    start_btn = framework.find_element_safe(
                        By.CSS_SELECTOR, "div#start button"
                    )
                    if start_btn:
                        start_btn.click()
                        print("⏳ Waiting for content to load...")
                        
                        # Wait for finish element
                        if framework.wait_for_element(By.ID, "finish", timeout=10):
                            finish_text = framework.get_element_text(
                                By.ID, "finish", "Finish message"
                            )
                            print(f"✅ Content loaded: {finish_text}")
                        else:
                            print("⚠️ Content did not load in time")
                
                elif 'hovers' in site['url']:
                    # Test hover functionality  
                    hover_elements = framework.driver.find_elements(
                        By.CSS_SELECTOR, ".figure"
                    )
                    
                    for j, element in enumerate(hover_elements[:2], 1):
                        if framework.hover_element(
                            By.CSS_SELECTOR, f".figure:nth-child({j})",
                            f"Hover image {j}"
                        ):
                            print(f"✅ Hover {j} successful")
                
                framework.take_screenshot(f"mini_test_{i}")
                time.sleep(2)  # Brief pause between tests
                
            else:
                print(f"❌ Failed to navigate to {site['name']}")
        
        print("\n🎉 Mini test suite completed!")
        
    except Exception as e:
        print(f"❌ Mini test suite error: {str(e)}")
        
    finally:
        framework.close_browser()


def main():
    """🎯 Main demo execution"""
    
    print("🚀 Welcome to Selenium Testing Framework Demo!")
    print("\nChoose demo type:")
    print("1. 💫 Quick Demo (5 minutes)")
    print("2. 🧪 Mini Test Suite (3 minutes)")  
    print("3. 🚀 Both demos")
    
    try:
        choice = input("\nEnter choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            run_quick_demo()
        elif choice == "2":
            run_mini_test_suite()
        elif choice == "3":
            run_quick_demo()
            print("\n" + "="*50)
            run_mini_test_suite()
        else:
            print("Invalid choice. Running quick demo...")
            run_quick_demo()
            
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        
    print("\n👋 Thanks for trying the Selenium Testing Framework!")
    print("📖 Run 'python main_test_runner.py' for the full test suite")


if __name__ == "__main__":
    main()