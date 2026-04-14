# 🕷️ Selenium Testing Suite
## Cross-Browser • Web Automation • Data Extraction • Screenshot Capture

Professional web automation framework supporting multiple browsers, comprehensive testing scenarios, and advanced data extraction capabilities. Built for enterprise web testing, UI automation, and data scraping workflows.

## ⭐ Key Features

### ✅ Multi-Browser Support  
- **Chrome** - Fast and reliable testing (default)
- **Firefox** - Cross-browser compatibility validation
- **Edge** - Microsoft ecosystem integration
- **Headless Mode** - CI/CD pipeline integration and background operations

### ✅ Professional Testing Framework
- **Page Object Model** - Maintainable test architecture
- **Explicit Waits** - Reliable element interaction handling  
- **Screenshot Capture** - Automatic failure documentation
- **Test Reports** - Comprehensive HTML reporting with pytest-html

### ✅ Advanced Data Extraction
- **Multi-Site Scraping** - The Internet Herokuapp and DemoQA integration
- **Dynamic Content** - JavaScript-rendered content handling
- **Form Automation** - Complex form filling and submission
- **Table Extraction** - Structured data extraction to CSV/JSON

### ✅ Enterprise Integration
- **Configuration-Driven** - External config files for easy customization
- **Comprehensive Logging** - Timestamped logs with emoji console output
- **Error Recovery** - Automatic retry mechanisms and graceful degradation  
- **CI/CD Ready** - Command-line interface with flexible options

## 📁 Project Structure

```
selenium Testing/
├── README.md                        # 📖 This documentation
├── requirements.txt                 # 📦 Selenium dependencies
├── selenium_framework.py            # 🎯 Main automation framework
├── config.py                        # ⚙️ Testing configuration
├── main_test_runner.py              # 🚀 Test orchestrator
├── web_scraper.py                   # 🕷️ The Internet Herokuapp scraper
├── advanced_data_extractor.py       # 🔍 Advanced extraction demos
├── quick_demo.py                    # 🎯 Quick start demonstration
├── logs/                            # 📝 Test execution logs 
│   ├── selenium_test_YYYYMMDD_HHMMSS.log
│   └── error_logs/
├── screenshots/                     # 📸 Test failure screenshots
│   └── selenium_test_YYYYMMDD_HHMMSS/
└── extraction_results/              # 📊 Scraping outputs
    ├── extraction_report.json
    └── extraction_summary.csv
```

## 🚀 Quick Start

### 1. Installation & Setup
```bash
# Install Selenium and dependencies
pip install -r requirements.txt

# Download WebDriver (automatically handled by selenium-manager in Selenium 4.15+)
# Or manually install ChromeDriver, GeckoDriver, EdgeDriver

# Verify installation
python -c "from selenium import webdriver; print('✅ Selenium ready')"
```

### 2. Quick Demo
```bash  
# Start with the quick demo
python quick_demo.py

# Run comprehensive test suite
python main_test_runner.py

# Extract data from The Internet Herokuapp
python web_scraper.py
```

### 3. Basic Usage
```python
from selenium_framework import SeleniumTestFramework

# Initialize framework
framework = SeleniumTestFramework(browser='chrome', headless=False)

# Navigate and interact
framework.navigate_to_url("https://the-internet.herokuapp.com", display=True)
framework.click_element("link text", "Dynamic Loading")
framework.take_screenshot()

# Cleanup
framework.quit()
```

## 🎯 Selenium Test Framework

### Core Class: `SeleniumTestFramework`

```python
class SeleniumTestFramework:
    def __init__(self, browser: str = 'chrome', headless: bool = False, 
                 window_width: int = 1920, window_height: int = 1080)
```

### Available Methods

| Method | Purpose | Parameters | Returns |
|--------|---------|------------|---------|  
| `navigate_to_url()` | Navigate to URL | `url, display` | Success status |
| `find_element()` | Locate element | `by_type, value` | WebElement |
| `click_element()` | Click element | `by_type, value` | Success status |
| `input_text()` | Enter text | `by_type, value, text` | Success status |
| `wait_for_element()` | Wait for element | `by_type, value, timeout` | WebElement |
| `take_screenshot()` | Capture screen | `filename` | Screenshot path |
| `extract_table()` | Extract table data | `table_selector` | List of rows |
| `get_page_source()` | Get HTML source | None | HTML string |

### Browser Options

```python
# Chrome (default)
framework = SeleniumTestFramework(browser='chrome')

# Firefox  
framework = SeleniumTestFramework(browser='firefox')

# Edge
framework = SeleniumTestFramework(browser='edge')

# Headless mode (any browser)
framework = SeleniumTestFramework(browser='chrome', headless=True)

# Custom window size
framework = SeleniumTestFramework(window_width=1366, window_height=768)
```

## 🌐 Web Scraping Examples

### 1. The Internet Herokuapp Scraper

```python
from web_scraper import InternetHerokuppScraper

# Initialize scraper
scraper = InternetHerokuppScraper(headless=True)

# Extract all data 
scraper.extract_all_data()

# Results saved to extraction_results/
```

**Extracted Data:**
- ✅ **Navigation Links** - All main page links and descriptions
- ✅ **Form Elements** - Input fields, dropdowns, checkboxes
- ✅ **Dynamic Content** - AJAX-loaded content and interactions
- ✅ **Tables** - Sortable table data with headers
- ✅ **Authentication** - Login form testing and validation

**Output Files:**
```json
// extraction_report.json
{
    "navigation_links": [...],
    "form_elements": [...], 
    "dynamic_content": [...],
    "table_data": [...],
    "extraction_summary": {...}
}
```

### 2. Advanced Data Extraction

```python
def extract_ecommerce_data():
    """Extract product data from e-commerce site"""
    
    framework = SeleniumTestFramework(browser='chrome', headless=True)
    
    try:
        # Navigate to product page
        framework.navigate_to_url("https://demowebshop.tricentis.com/")
        
        # Extract product information
        products = []
        product_elements = framework.driver.find_elements(By.CLASS_NAME, "product-item")
        
        for product in product_elements:
            product_data = {
                'name': product.find_element(By.CLASS_NAME, "product-title").text,
                'price': product.find_element(By.CLASS_NAME, "price").text,
                'rating': len(product.find_elements(By.CLASS_NAME, "rating-star"))
            }
            products.append(product_data)
        
        # Save to DataFrame
        df = pd.DataFrame(products)
        df.to_csv('extraction_results/products.csv', index=False)
        
        print(f"✅ Extracted {len(products)} products")
        return products
        
    finally:
        framework.quit()
```

### 3. Form Automation

```python
def automated_form_submission():
    """Automated form filling and submission"""
    
    framework = SeleniumTestFramework(browser='chrome')
    
    # Navigate to form
    framework.navigate_to_url("https://demoqa.com/automation-practice-form")
    
    # Fill form fields
    form_data = {
        'firstName': 'John',
        'lastName': 'Doe', 
        'userEmail': 'john.doe@example.com',
        'userNumber': '1234567890'
    }
    
    for field_id, value in form_data.items():
        framework.input_text("id", field_id, value)
    
    # Select gender radio button
    framework.click_element("label", "Male")
    
    # Select date of birth
    framework.click_element("id", "dateOfBirthInput")
    framework.click_element("class name", "react-datepicker__year-select")
    framework.click_element("xpath", "//option[@value='1990']")
    
    # Submit form
    framework.click_element("id", "submit")
    
    # Verify submission
    success_message = framework.wait_for_element("id", "example-modal-sizes-title-lg")
    if success_message:
        print("✅ Form submitted successfully")
        framework.take_screenshot("form_submission_success")
    
    framework.quit()
```

## ⚙️ Configuration Management

### Configuration Class: `SeleniumConfig`

```python
# config.py contains comprehensive configuration
from config import SeleniumConfig

# Browser settings
SeleniumConfig.BROWSERS = {
    'chrome': {'window_size': (1920, 1080), 'headless': False},
    'firefox': {'window_size': (1920, 1080), 'headless': False}, 
    'edge': {'window_size': (1920, 1080), 'headless': False}
}

# Timing configuration
SeleniumConfig.TIMEOUTS = {
    'implicit_wait': 10,
    'explicit_wait': 20, 
    'page_load': 30,
    'script': 30
}

# Test URLs
SeleniumConfig.TEST_URLS = {
    'herokuapp': 'https://the-internet.herokuapp.com',
    'demoqa': 'https://demoqa.com',
    'demoshop': 'https://demowebshop.tricentis.com'
}
```

### Environment-Based Configuration

```python
import os

# Override configuration via environment
browser = os.getenv('SELENIUM_BROWSER', 'chrome')
headless = os.getenv('SELENIUM_HEADLESS', 'false').lower() == 'true'
implicit_wait = int(os.getenv('SELENIUM_WAIT', '10'))

framework = SeleniumTestFramework(
    browser=browser,
    headless=headless
)
framework.driver.implicitly_wait(implicit_wait)
```

## 🧪 Test Runner & Orchestration  

### Main Test Runner

```bash
# Run all tests with default settings
python main_test_runner.py

# Specify browser 
python main_test_runner.py --browser firefox

# Headless mode
python main_test_runner.py --headless

# Custom test suite
python main_test_runner.py --suite smoke_tests

# Generate HTML report
python main_test_runner.py --report
```

### Test Suite Organization

```python
class SeleniumTestRunner:
    def __init__(self, browser='chrome', headless=False):
        self.test_suites = {
            'smoke_tests': [
                self.test_navigation,
                self.test_form_interaction, 
                self.test_screenshot_capture
            ],
            'full_tests': [
                self.test_all_browsers,
                self.test_data_extraction,
                self.test_error_handling,
                self.test_performance
            ],
            'extraction_tests': [
                self.test_herokuapp_scraping,
                self.test_table_extraction,
                self.test_dynamic_content
            ]
        }
    
    def run_test_suite(self, suite_name='full_tests'):
        """Run specified test suite"""
        
        tests = self.test_suites.get(suite_name, [])
        results = {'passed': 0, 'failed': 0, 'errors': []}
        
        for test in tests:
            try:
                test()
                results['passed'] += 1
                print(f"✅ {test.__name__} - PASSED")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{test.__name__}: {str(e)}")
                print(f"❌ {test.__name__} - FAILED: {str(e)}")
        
        return results
```

## 📸 Screenshot & Reporting  

### Automatic Screenshot Capture

```python
def test_with_screenshots():
    """Test with automatic screenshot capture"""
    
    framework = SeleniumTestFramework(browser='chrome')
    
    try:
        # Navigate and capture
        framework.navigate_to_url("https://demoqa.com") 
        framework.take_screenshot("homepage")
        
        # Interact and capture
        framework.click_element("text", "Elements")
        framework.take_screenshot("elements_page")
        
        # Error scenario with screenshot  
        try:
            framework.click_element("id", "nonexistent_element")
        except Exception as e:
            framework.take_screenshot("error_scenario")
            print(f"❌ Error captured: {str(e)}")
    
    finally:
        framework.quit()
```

**Screenshot Organization:**
```
screenshots/
├── selenium_test_20260414_143022/
│   ├── homepage.png
│   ├── elements_page.png 
│   ├── error_scenario.png
│   └── test_summary.json
└── selenium_test_20260414_150125/
    └── ...
```

### Test Reporting

```python
def generate_test_report(results: dict):
    """Generate comprehensive test report"""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_tests': results['passed'] + results['failed'],
            'passed': results['passed'],
            'failed': results['failed'],
            'success_rate': results['passed'] / (results['passed'] + results['failed']) * 100
        },
        'errors': results['errors'],
        'screenshots': glob.glob('screenshots/**/*.png', recursive=True),
        'logs': glob.glob('logs/*.log')
    }
    
    # Save as JSON
    with open('extraction_results/test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Generate HTML report
    html_report = f"""
    <html>
    <head><title>Selenium Test Report</title></head>
    <body>
        <h1>Test Execution Report</h1>
        <p><strong>Success Rate:</strong> {report['summary']['success_rate']:.1f}%</p>
        <p><strong>Tests Passed:</strong> {report['summary']['passed']}</p>
        <p><strong>Tests Failed:</strong> {report['summary']['failed']}</p>
        <h2>Screenshots</h2>
        {''.join([f'<img src="{img}" width="300px">' for img in report['screenshots']])}
    </body>
    </html>
    """
    
    with open('extraction_results/test_report.html', 'w') as f:
        f.write(html_report)
```

## 🚨 Error Handling & Recovery

### Robust Element Interaction

```python
def safe_element_interaction(framework, by_type, value, action='click', text=None, max_retries=3):
    """Perform element interaction with retry logic"""
    
    for attempt in range(max_retries):
        try:
            # Wait for element
            element = framework.wait_for_element(by_type, value)
            
            # Scroll into view
            framework.driver.execute_script("arguments[0].scrollIntoView();", element)
            
            # Perform action
            if action == 'click':
                element.click()
            elif action == 'input' and text:
                element.clear()
                element.send_keys(text)
            elif action == 'select' and text:
                select = Select(element)
                select.select_by_visible_text(text)
            
            return True
            
        except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            print(f"⚠️ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                framework.take_screenshot(f"error_{by_type}_{value}")
                raise e
    
    return False
```

### Browser Recovery

```python
def browser_health_check(framework):
    """Check browser health and recover if needed"""
    
    try:
        # Test basic functionality
        framework.driver.execute_script("return document.readyState")
        framework.driver.current_url
        return True
        
    except (WebDriverException, InvalidSessionIdException):
        print("🔄 Browser session lost, attempting recovery...")
        
        try:
            framework.quit()
            framework.__init__(framework.browser, framework.headless) 
            return True
        except Exception as e:
            print(f"❌ Browser recovery failed: {str(e)}")
            return False
```

## ⚡ Performance Optimization

### Page Load Monitoring

```python
def monitor_page_performance(framework, url):
    """Monitor page load performance"""
    
    # Start timing
    start_time = time.time()
    
    # Navigate to page
    framework.navigate_to_url(url, display=True)
    
    # Wait for complete load
    WebDriverWait(framework.driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    
    # Calculate metrics 
    load_time = time.time() - start_time
    
    # Get performance metrics via JavaScript
    navigation_timing = framework.driver.execute_script("""
        var timing = performance.timing;
        return {
            'dns_lookup': timing.domainLookupEnd - timing.domainLookupStart,
            'connection': timing.connectEnd - timing.connectStart,
            'response': timing.responseEnd - timing.responseStart,
            'dom_processing': timing.domComplete - timing.domLoading
        };
    """)
    
    performance_data = {
        'url': url,
        'total_load_time': load_time,
        'navigation_timing': navigation_timing,
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"📊 Page load time: {load_time:.2f}s")
    return performance_data
```

### Memory Usage Monitoring  

```python
import psutil

def monitor_browser_resources():
    """Monitor browser resource usage"""
    
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    framework = SeleniumTestFramework(browser='chrome')
    
    # Perform operations
    for i in range(10):
        framework.navigate_to_url("https://the-internet.herokuapp.com")
        current_memory = process.memory_info().rss / 1024 / 1024
        print(f"🧠 Memory usage after {i+1} navigations: {current_memory:.1f} MB")
    
    framework.quit()
    
    final_memory = process.memory_info().rss / 1024 / 1024
    print(f"📊 Memory cleanup: {initial_memory:.1f} → {final_memory:.1f} MB")
```

## 🏢 Enterprise Integration

### CI/CD Pipeline Integration

```yaml
# .github/workflows/selenium-tests.yml  
name: Selenium UI Tests
on: [push, pull_request]
jobs:
  selenium-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          sudo apt-get update
          sudo apt-get install -y chromium-browser
      - name: Run Selenium tests
        run: python main_test_runner.py --headless --browser chrome
        env:
          SELENIUM_HEADLESS: true
      - name: Upload screenshots  
        uses: actions/upload-artifact@v2
        if: failure()
        with:
          name: selenium-screenshots
          path: screenshots/
```

### Docker Integration

```dockerfile
# Dockerfile for Selenium testing
FROM python:3.9-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run tests
CMD ["python", "main_test_runner.py", "--headless", "--browser", "chrome"]
```

### Parallel Test Execution

```python
from concurrent.futures import ThreadPoolExecutor
import threading

def run_parallel_tests(test_urls, max_workers=3):
    """Run tests in parallel across multiple browsers"""
    
    results = {}
    lock = threading.Lock()
    
    def run_single_test(url):
        thread_id = threading.get_ident()
        framework = SeleniumTestFramework(browser='chrome', headless=True)
        
        try:
            # Add thread safety for logging
            with lock:
                print(f"🔄 Thread {thread_id}: Testing {url}")
            
            framework.navigate_to_url(url)
            success = framework.wait_for_element("body", timeout=10) is not None
            
            with lock:
                results[url] = {'success': success, 'thread': thread_id}
                
        except Exception as e:
            with lock:
                results[url] = {'success': False, 'error': str(e), 'thread': thread_id}
        finally:
            framework.quit()
    
    # Execute tests in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(run_single_test, test_urls)
    
    return results
```

## 🔧 Troubleshooting

### Common WebDriver Issues  

**1. WebDriver Not Found**
```python
# Selenium 4.15+ handles this automatically, but for older versions:
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

**2. Element Not Interactable**
```python
# Solution: Scroll into view and wait
def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
    element.click()
```

**3. Stale Element Reference**  
```python
# Solution: Re-locate element
def robust_element_interaction(driver, locator):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            element = driver.find_element(*locator)
            element.click()
            break
        except StaleElementReferenceException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(1)
```

### Performance Issues

**1. Slow Page Loads**
```python
# Optimize page load strategy
options = ChromeOptions()
options.add_argument("--page-load-strategy=eager")  # Don't wait for images
options.add_argument("--disable-images")
options.add_argument("--disable-javascript")  # If JS not needed
```

**2. Memory Leaks**
```python
# Proper cleanup and resource management
def cleanup_test_session(framework):
    try:
        # Clear browser data
        framework.driver.delete_all_cookies()
        framework.driver.execute_script("window.localStorage.clear();")
        framework.driver.execute_script("window.sessionStorage.clear();")
    finally:
        framework.quit()
```

## 📚 Additional Resources

### Related Documentation  
- 🚀 [API Testing](../API_Testing/README.md) - Test web APIs discovered through Selenium
- 🗄️ [Database Actions](../database_actions/README.md) - Store scraped data in databases
- 📊 [Pandas Analysis](../pandas_analysis/README.md) - Analyze extracted web data

### External References
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [WebDriver W3C Standard](https://www.w3.org/TR/webdriver/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [The Internet Herokuapp](https://the-internet.herokuapp.com/) - Practice site

---

**🕷️ Built for professional web automation and testing**

*Cross-Platform • Scalable • Enterprise-Ready* ✨