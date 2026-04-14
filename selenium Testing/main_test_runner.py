#!/usr/bin/env python3
"""
🚀 Selenium Testing Suite Runner
===============================

Main orchestrator for comprehensive Selenium automation testing
across multiple free websites and scenarios.

This runner executes:
- The Internet Herokuapp tests (forms, dynamic content, alerts)
- DemoQA tests (UI elements, interactions, widgets)  
- E-Commerce tests (shopping workflows, cart operations)

Features:
- Multi-browser support (Chrome, Firefox, Edge)
- Headless mode option
- Comprehensive reporting
- Screenshot capture
- Detailed logging
- Error recovery
- Performance metrics

Usage:
    python main_test_runner.py --browser chrome --headless
    python main_test_runner.py --browser firefox
    python main_test_runner.py --help

Author: AI Assistant
Date: 2024-04-10  
"""

import argparse
import sys
import time
from datetime import datetime
import os
from typing import Dict, List

# Import our test suites
from selenium_framework import SeleniumTestFramework
from test_herokuapp import TheInternetTests
from test_demoqa import DemoQATests
from test_ecommerce import ECommerceTests


class SeleniumTestRunner:
    """🎯 Main test runner orchestrating all Selenium test suites"""
    
    def __init__(self, browser: str = "chrome", headless: bool = False):
        """
        Initialize the test runner
        
        Args:
            browser (str): Browser choice (chrome, firefox, edge)
            headless (bool): Run in headless mode
        """
        self.browser = browser
        self.headless = headless
        self.framework = None
        self.test_start_time = None
        self.all_results = []
        
    def setup_environment(self):
        """🔧 Setup testing environment"""
        print("🚀 SELENIUM TESTING SUITE INITIALIZATION")
        print("=" * 60)
        print(f"🌐 Browser: {self.browser.upper()}")
        print(f"👁️ Headless Mode: {'ON' if self.headless else 'OFF'}")
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Initialize Selenium framework
        try:
            self.framework = SeleniumTestFramework(
                browser=self.browser,
                headless=self.headless,
                implicit_wait=10,
                explicit_wait=15
            )
            
            # Start browser
            self.framework.start_browser()
            print("✅ Browser initialized successfully")
            
            return True
            
        except Exception as e:
            print(f"❌ Environment setup failed: {str(e)}")
            return False
    
    def run_herokuapp_tests(self) -> Dict:
        """🌐 Execute The Internet Herokuapp test suite"""
        print("\n" + "🎯" + "=" * 58 + "🎯")
        print("   THE INTERNET HEROKUAPP - CHALLENGING SCENARIOS")
        print("🎯" + "=" * 58 + "🎯")
        
        try:
            herokuapp_tests = TheInternetTests(self.framework)
            herokuapp_tests.run_all_tests()
            
            return {
                'suite': 'The Internet Herokuapp',
                'results': herokuapp_tests.test_results,
                'status': '✅ COMPLETED'
            }
            
        except Exception as e:
            print(f"❌ Herokuapp tests failed: {str(e)}")
            return {
                'suite': 'The Internet Herokuapp', 
                'results': [],
                'status': f'❌ FAILED: {str(e)}'
            }
    
    def run_demoqa_tests(self) -> Dict:
        """🎨 Execute DemoQA UI elements test suite"""
        print("\n" + "🎯" + "=" * 58 + "🎯")
        print("        DEMOQA - UI ELEMENTS & INTERACTIONS")
        print("🎯" + "=" * 58 + "🎯")
        
        try:
            demoqa_tests = DemoQATests(self.framework)
            demoqa_tests.run_all_tests()
            
            return {
                'suite': 'DemoQA UI Elements',
                'results': demoqa_tests.test_results,
                'status': '✅ COMPLETED'
            }
            
        except Exception as e:
            print(f"❌ DemoQA tests failed: {str(e)}")
            return {
                'suite': 'DemoQA UI Elements',
                'results': [],
                'status': f'❌ FAILED: {str(e)}'
            }
    
    def run_ecommerce_tests(self) -> Dict:
        """🛒 Execute E-Commerce workflow test suite"""
        print("\n" + "🎯" + "=" * 58 + "🎯")
        print("       E-COMMERCE - SHOPPING WORKFLOWS")  
        print("🎯" + "=" * 58 + "🎯")
        
        try:
            ecommerce_tests = ECommerceTests(self.framework)
            ecommerce_tests.run_all_tests()
            
            return {
                'suite': 'E-Commerce Workflows',
                'results': ecommerce_tests.test_results,
                'status': '✅ COMPLETED'
            }
            
        except Exception as e:
            print(f"❌ E-Commerce tests failed: {str(e)}")
            return {
                'suite': 'E-Commerce Workflows',
                'results': [], 
                'status': f'❌ FAILED: {str(e)}'
            }
    
    def run_all_test_suites(self):
        """🚀 Execute all test suites in sequence"""
        self.test_start_time = time.time()
        
        # Test suites to execute
        test_suites = [
            ("🌐 Herokuapp Tests", self.run_herokuapp_tests),
            ("🎨 DemoQA Tests", self.run_demoqa_tests),
            ("🛒 E-Commerce Tests", self.run_ecommerce_tests)
        ]
        
        for suite_name, suite_method in test_suites:
            try:
                print(f"\n🔄 Starting {suite_name}...")
                
                suite_result = suite_method()
                self.all_results.append(suite_result)
                
                print(f"✅ {suite_name} completed")
                
                # Brief pause between test suites
                time.sleep(3)
                
            except KeyboardInterrupt:
                print(f"\n⚠️ Test suite interrupted by user")
                break
                
            except Exception as e:
                print(f"❌ {suite_name} encountered an error: {str(e)}")
                self.all_results.append({
                    'suite': suite_name,
                    'results': [],
                    'status': f'❌ ERROR: {str(e)}'
                })
    
    def generate_comprehensive_report(self):
        """📊 Generate detailed test execution report"""
        total_duration = time.time() - self.test_start_time
        
        print("\n" + "🎯" * 20)
        print("🎯" + " " * 16 + "FINAL TEST REPORT" + " " * 17 + "🎯")
        print("🎯" * 20)
        
        # Summary statistics
        total_tests = 0
        total_passed = 0
        
        for suite_result in self.all_results:
            print(f"\n📋 {suite_result['suite']}")
            print("-" * 50)
            print(f"Status: {suite_result['status']}")
            
            if suite_result['results']:
                suite_tests = len(suite_result['results'])
                suite_passed = sum(1 for test in suite_result['results'] if 'PASS' in test['status'])
                
                total_tests += suite_tests
                total_passed += suite_passed
                
                print(f"Tests: {suite_passed}/{suite_tests} passed ({(suite_passed/suite_tests*100):.1f}%)")
                
                # Show individual test results
                for test in suite_result['results']:
                    print(f"  {test['status']} {test['test']}")
            else:
                print("No test results available")
        
        # Overall statistics
        print("\n" + "=" * 60)
        print("📊 OVERALL TEST EXECUTION SUMMARY")
        print("=" * 60)
        
        print(f"🌐 Browser Used: {self.browser.upper()}")
        print(f"👁️ Headless Mode: {'Enabled' if self.headless else 'Disabled'}")
        print(f"⏱️ Total Duration: {total_duration:.2f} seconds ({total_duration/60:.1f} minutes)")
        print(f"📋 Total Test Suites: {len(self.all_results)}")
        print(f"🎯 Total Individual Tests: {total_tests}")
        print(f"✅ Tests Passed: {total_passed}")
        print(f"❌ Tests Failed: {total_tests - total_passed}")
        
        if total_tests > 0:
            success_rate = (total_passed / total_tests) * 100
            print(f"📈 Overall Success Rate: {success_rate:.1f}%")
            
            # Performance rating
            if success_rate >= 95:
                rating = "🏆 EXCELLENT - Master Level Automation!"
            elif success_rate >= 85:
                rating = "🥇 VERY GOOD - Advanced Automation Skills!"  
            elif success_rate >= 70:
                rating = "🥈 GOOD - Solid Automation Foundation!"
            elif success_rate >= 50:
                rating = "🥉 FAIR - Keep Practicing!"
            else:
                rating = "📚 NEEDS IMPROVEMENT - More Learning Required!"
                
            print(f"🏅 Performance Rating: {rating}")
        
        # Test environment info
        print(f"\n🔧 Test Environment:")
        print(f"   📂 Screenshots saved in: screenshots/")
        print(f"   📄 Logs saved in: logs/")  
        print(f"   🕒 Test execution completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "🎯" * 20)
        print("Thank you for using the Selenium Testing Suite! 🚀")
        print("🎯" * 20)
    
    def cleanup(self):
        """🧹 Cleanup resources"""
        try:
            if self.framework:
                self.framework.close_browser()
            print("\n🧹 Cleanup completed successfully")
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {str(e)}")
    
    def run(self):
        """▶️ Main execution method"""
        try:
            # Setup environment
            if not self.setup_environment():
                return False
            
            # Execute all test suites
            self.run_all_test_suites()
            
            # Generate report
            self.generate_comprehensive_report()
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️ Testing interrupted by user")
            return False
            
        except Exception as e:
            print(f"\n❌ Unexpected error during test execution: {str(e)}")
            return False
            
        finally:
            self.cleanup()


def parse_arguments():
    """📝 Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="🚀 Selenium Testing Suite - Comprehensive Web Automation Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_test_runner.py --browser chrome
  python main_test_runner.py --browser firefox --headless
  python main_test_runner.py --browser edge --headless

Supported Browsers:
  - chrome (default)
  - firefox  
  - edge

Free Testing Websites Used:
  - https://the-internet.herokuapp.com/ (Challenging scenarios)
  - https://demoqa.com/ (UI elements & interactions)
  - https://automationpractice.com/ (E-commerce workflows)
        """
    )
    
    parser.add_argument(
        '--browser', '-b',
        choices=['chrome', 'firefox', 'edge'],
        default='chrome',
        help='Browser to use for testing (default: chrome)'
    )
    
    parser.add_argument(
        '--headless', '-h',
        action='store_true',
        help='Run browser in headless mode (no GUI)'
    )
    
    return parser.parse_args()


def main():
    """🎯 Main entry point"""
    # Parse arguments
    args = parse_arguments()
    
    # Create and run test suite
    runner = SeleniumTestRunner(
        browser=args.browser,
        headless=args.headless
    )
    
    success = runner.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()