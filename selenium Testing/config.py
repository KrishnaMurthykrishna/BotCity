#!/usr/bin/env python3
"""
🔧 Selenium Testing Configuration
=================================

Configuration settings for the Selenium Testing Suite.
Modify these settings to customize test execution behavior.

Author: AI Assistant
Date: 2024-04-10
"""

# 🌐 Browser Configuration
BROWSER_CONFIG = {
    'default_browser': 'chrome',
    'headless_mode': False,
    'window_size': (1920, 1080),
    'implicit_wait': 10,
    'explicit_wait': 15,
    'page_load_timeout': 30
}

# ⏱️ Timing Configuration  
TIMING_CONFIG = {
    'short_wait': 1,        # Brief pause between actions
    'medium_wait': 3,       # Wait for page elements
    'long_wait': 5,         # Wait for complex operations
    'test_suite_pause': 3   # Pause between test suites
}

# 📸 Screenshot Configuration
SCREENSHOT_CONFIG = {
    'enabled': True,
    'on_failure': True,
    'directory': 'screenshots',
    'format': 'png',
    'timestamp_format': '%Y%m%d_%H%M%S'
}

# 📝 Logging Configuration
LOGGING_CONFIG = {
    'enabled': True,
    'level': 'INFO',        # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'directory': 'logs',
    'file_format': 'selenium_testing_{timestamp}.log',
    'console_output': True,
    'detailed_traceback': True
}

# 🌐 Test Website URLs
TEST_URLS = {
    'herokuapp': {
        'base': 'https://the-internet.herokuapp.com',
        'timeout': 30,
        'retry_attempts': 3
    },
    'demoqa': {
        'base': 'https://demoqa.com',
        'timeout': 30,
        'retry_attempts': 3
    },
    'ecommerce_primary': {
        'base': 'https://automationpractice.com',
        'timeout': 30,
        'retry_attempts': 2
    },
    'ecommerce_backup': {
        'base': 'https://practice.automationtesting.in',
        'timeout': 30,
        'retry_attempts': 2
    }
}

# 🎯 Test Execution Configuration
EXECUTION_CONFIG = {
    'stop_on_first_failure': False,
    'retry_failed_tests': True,
    'max_retry_attempts': 2,
    'parallel_execution': False,
    'test_data_cleanup': True
}

# 📊 Reporting Configuration  
REPORTING_CONFIG = {
    'generate_html_report': True,
    'include_screenshots': True,
    'include_performance_metrics': True,
    'email_results': False,
    'export_to_excel': False
}

# 🧪 Test Data Configuration
TEST_DATA = {
    'user_credentials': {
        'test_email': 'selenium.tester@example.com',
        'test_password': 'TestPass123!',
        'test_username': 'selenium_user'
    },
    'form_data': {
        'first_name': 'John',
        'last_name': 'Doe', 
        'company': 'Test Company',
        'address': '123 Test Street',
        'city': 'Test City',
        'postal_code': '12345',
        'phone': '+1-555-0123'
    },
    'search_terms': ['dress', 'shirt', 'shoes', 'electronics'],
    'file_upload': {
        'test_file_name': 'selenium_test_file.txt',
        'test_file_content': 'This is a test file for Selenium automation.'
    }
}

# 🔧 Browser-Specific Options
BROWSER_OPTIONS = {
    'chrome': {
        'arguments': [
            '--no-sandbox',
            '--disable-dev-shm-usage', 
            '--disable-gpu',
            '--disable-web-security',
            '--allow-running-insecure-content',
            '--start-maximized',
            '--disable-blink-features=AutomationControlled'
        ],
        'prefs': {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0
        }
    },
    'firefox': {
        'arguments': [
            '--width=1920',
            '--height=1080'
        ],
        'preferences': {
            'dom.webnotifications.enabled': False,
            'dom.push.enabled': False
        }
    },
    'edge': {
        'arguments': [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--start-maximized'
        ]
    }
}

# 🎮 Advanced Configuration
ADVANCED_CONFIG = {
    'custom_user_agent': 'Selenium Testing Suite 1.0',
    'disable_images': False,      # Speed up page loading
    'disable_css': False,         # Further speed improvement  
    'enable_performance_logging': True,
    'capture_network_logs': False,
    'mobile_emulation': {
        'enabled': False,
        'device_name': 'iPhone 12'
    }
}

# 🚨 Error Handling Configuration
ERROR_CONFIG = {
    'continue_on_element_not_found': True,
    'continue_on_timeout': True,
    'continue_on_javascript_error': True,
    'max_consecutive_failures': 5,
    'auto_recovery_attempts': 3
}

# 📧 Notification Configuration (Optional)
NOTIFICATION_CONFIG = {
    'email_enabled': False,
    'email_recipients': ['test-results@example.com'],
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'slack_webhook': None,      # Slack webhook URL for notifications
    'teams_webhook': None       # Microsoft Teams webhook URL
}

# 🏷️ Test Categories Configuration
TEST_CATEGORIES = {
    'smoke_tests': {
        'enabled': True,
        'description': 'Basic functionality verification'
    },
    'regression_tests': {
        'enabled': True, 
        'description': 'Comprehensive feature testing'
    },
    'performance_tests': {
        'enabled': False,
        'description': 'Page load and response time testing'
    },
    'accessibility_tests': {
        'enabled': False,
        'description': 'Accessibility compliance testing'
    }
}