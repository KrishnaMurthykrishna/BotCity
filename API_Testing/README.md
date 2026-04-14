# 🚀 API Testing Suite
## REST API Framework • HTTP Methods • Error Injection • Public API Examples

Professional REST API testing framework with comprehensive HTTP method support, error injection capabilities, and real-world public API examples. Built for enterprise API validation, integration testing, and automated service monitoring.

## ⭐ Key Features

### ✅ Complete HTTP Method Support
- **GET** - Data retrieval with query parameters
- **POST** - Data creation with JSON/form data
- **PUT** - Full resource updates  
- **PATCH** - Partial resource modifications
- **DELETE** - Resource removal operations

### ✅ Advanced Request Handling  
- **Query Parameters** - URL parameter encoding
- **JSON Data** - Structured data payloads
- **Form Data** - application/x-www-form-urlencoded
- **Headers Management** - Custom headers and authentication
- **SSL Configuration** - Certificate handling and verification control

### ✅ Professional Error Management
- **Error Injection** - Simulate timeout, connection, and HTTP errors
- **Retry Logic** - Configurable retry mechanisms with exponential backoff
- **Graceful Fallbacks** - Handle network issues and service unavailability
- **Comprehensive Logging** - File and console logging with detailed error tracking

### ✅ Real-World API Testing
- **JSONPlaceholder** - Complete CRUD operations demo
- **HTTPBin** - Request/response testing and validation
- **ReqRes** - User management API scenarios  
- **Cat Facts API** - Public data consumption examples

## 📁 Project Structure

```
API_Testing/
├── README.md                    # 📖 This documentation
├── REST_API_Testing.py          # 🎯 Main API testing framework
├── Free_API_Examples.py         # 🌐 Public API demonstrations
├── HTTP_API_Examples.py         # 🔐 Non-SSL HTTP examples
└── logs/                        # 📝 Test execution logs
    ├── api_test_YYYYMMDD_HHMMSS.log
    └── error_logs/
```

## 🚀 Quick Start

### 1. Installation
```bash
# Install dependencies
pip install requests>=2.31.0 urllib3 certifi

# Verify installation
python -c "import requests; print('✅ Ready for API testing')"
```

### 2. Basic Usage
```python
from REST_API_Testing import APITestFramework

# Initialize framework
api = APITestFramework(base_url="https://jsonplaceholder.typicode.com")

# Simple GET request
result = api.get_request("/posts/1")
print(f"Status: {result['status_code']}, Response: {result['response']}")

# POST with JSON data
data = {"title": "Test Post", "body": "Test content", "userId": 1}
result = api.post_request("/posts", json_data=data)

# Cleanup
api.close()
```

### 3. Run Complete Examples
```bash
# Test all public APIs
python Free_API_Examples.py

# HTTP-only examples (corporate environments)  
python HTTP_API_Examples.py

# Individual framework testing
python REST_API_Testing.py
```

## 🎯 API Testing Framework

### Core Class: `APITestFramework`

```python
class APITestFramework:
    def __init__(self, base_url: str, verify_ssl: bool = True, timeout: int = 30)
```

### Available Methods

| Method | Purpose | Parameters | Returns |
|--------|---------|------------|---------|
| `get_request()` | Retrieve data | `endpoint, params, headers` | Response dict |
| `post_request()` | Create data | `endpoint, json_data, form_data, headers` | Response dict |
| `put_request()` | Full update | `endpoint, json_data, form_data, headers` | Response dict |
| `patch_request()` | Partial update | `endpoint, json_data, form_data, headers` | Response dict |
| `delete_request()` | Remove data | `endpoint, headers` | Response dict |
| `generate_test_error()` | Error injection | `error_type` | Error response |

### Response Format
```python
{
    'success': bool,           # Request success status
    'status_code': int,        # HTTP status code  
    'response': dict|str,      # Response data
    'headers': dict,           # Response headers
    'timing': float,           # Response time in seconds
    'error': str|None          # Error message if failed
}
```

## 🌐 Public API Examples

### 1. JSONPlaceholder - Complete CRUD Demo

```python
from Free_API_Examples import test_jsonplaceholder_crud

# Full CRUD workflow
test_jsonplaceholder_crud()
```

**Operations Covered:**
- ✅ GET all posts (pagination handling)
- ✅ GET single post by ID
- ✅ POST new post creation
- ✅ PUT full post update  
- ✅ PATCH partial post update
- ✅ DELETE post removal

### 2. HTTPBin - Request/Response Testing

```python  
from Free_API_Examples import test_httpbin_methods

# HTTP method validation
test_httpbin_methods()
```

**Features Tested:**
- ✅ GET with query parameters
- ✅ POST with JSON and form data
- ✅ Headers echoing and validation
- ✅ User-Agent and IP detection
- ✅ Response format validation

### 3. ReqRes - User Management API

```python
from Free_API_Examples import test_reqres_users

# User CRUD operations  
test_reqres_users()
```

**User Operations:**
- ✅ List users with pagination
- ✅ Get single user details
- ✅ Create new user
- ✅ Update user information
- ✅ Delete user account

### 4. Cat Facts API - Data Consumption

```python
from Free_API_Examples import test_catfacts_api

# Public data API testing
test_catfacts_api()
```

**Data Operations:**
- ✅ Random cat facts retrieval
- ✅ Paginated facts listing
- ✅ Response validation and parsing

## 🚨 Error Injection & Testing

### Available Error Types

```python
api = APITestFramework("https://httpbin.org")

# Test different error scenarios
timeout_error = api.generate_test_error("timeout")
connection_error = api.generate_test_error("connection") 
invalid_url_error = api.generate_test_error("invalid_url")
json_error = api.generate_test_error("invalid_json")
http_error = api.generate_test_error("http_error")
random_error = api.generate_test_error("random")
```

### Error Response Format
```python
{
    'success': False,
    'status_code': None,
    'response': None, 
    'headers': {},
    'timing': 0.0,
    'error': 'Detailed error description'
}
```

### Error Handling Best Practices

```python
# Robust error handling example
def safe_api_call():
    api = APITestFramework("https://api.example.com")
    
    try:
        result = api.get_request("/data")
        if result['success']:
            return result['response']
        else:
            print(f"❌ API Error: {result['error']}")
            return None
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        return None
    finally:
        api.close()
```

## 📊 Advanced Configuration

### Custom Headers & Authentication

```python
# API key authentication
headers = {
    'Authorization': 'Bearer your-api-token',
    'Content-Type': 'application/json',
    'User-Agent': 'YourApp/1.0'
}

result = api.get_request("/protected", headers=headers)
```

### SSL Configuration

```python
# Disable SSL verification (corporate environments)
api = APITestFramework(
    base_url="http://internal-api.company.com",
    verify_ssl=False,
    timeout=60
)
```

### Batch Testing

```python
def run_api_test_suite():
    """Run comprehensive API test suite"""
    
    test_scenarios = [
        ("JSONPlaceholder CRUD", test_jsonplaceholder_crud),
        ("HTTPBin Methods", test_httpbin_methods), 
        ("ReqRes Users", test_reqres_users),
        ("Cat Facts API", test_catfacts_api)
    ]
    
    results = {}
    for name, test_func in test_scenarios:
        try:
            print(f"🔄 Running {name}...")
            test_func()
            results[name] = "✅ PASSED"
        except Exception as e:
            results[name] = f"❌ FAILED: {str(e)}"
    
    return results
```

## 📝 Logging Configuration

### Automatic Logging Features
- ✅ **Timestamped files** - `api_test_YYYYMMDD_HHMMSS.log`
- ✅ **Console output** - Real-time emoji-enhanced progress
- ✅ **Error tracking** - Detailed error logs with stack traces  
- ✅ **Request/Response logging** - Complete HTTP transaction logs
- ✅ **Performance metrics** - Response times and success rates

### Sample Log Output
```
2026-04-14 10:30:15 - INFO - 🚀 Starting API Test Framework
2026-04-14 10:30:15 - INFO - 🌐 Testing JSONPlaceholder API  
2026-04-14 10:30:16 - INFO - ✅ GET /posts/1 - 200 OK (0.234s)
2026-04-14 10:30:17 - INFO - ✅ POST /posts - 201 Created (0.456s)
2026-04-14 10:30:17 - ERROR - ❌ Timeout error simulated - Request timeout after 0.1s
```

## 🔧 Troubleshooting

### Common Issues

**1. SSL Certificate Errors**
```python
# Solution: Disable SSL verification
api = APITestFramework(base_url="https://api.com", verify_ssl=False)
```

**2. Connection Timeouts** 
```python
# Solution: Increase timeout
api = APITestFramework(base_url="https://api.com", timeout=120)
```

**3. JSON Parsing Errors**
```python
# Solution: Check response content type
result = api.get_request("/endpoint")
if result['success']:
    content_type = result['headers'].get('content-type', '')
    if 'application/json' in content_type:
        data = result['response']
    else:
        print("⚠️ Non-JSON response received")
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enables detailed request/response logging
api = APITestFramework("https://httpbin.org")
```

## 📈 Performance Monitoring

### Timing Analysis
```python
# Track API performance
start_time = time.time()
result = api.get_request("/large-dataset")
end_time = time.time()

if result['timing'] > 5.0:
    print(f"⚠️ Slow API response: {result['timing']:.2f}s")
```

### Batch Performance Testing
```python
def performance_benchmark(api_endpoint: str, iterations: int = 100):
    """Benchmark API performance"""
    
    api = APITestFramework("https://jsonplaceholder.typicode.com")
    times = []
    
    for i in range(iterations):
        result = api.get_request(api_endpoint)
        if result['success']:
            times.append(result['timing'])
    
    avg_time = sum(times) / len(times) if times else 0
    print(f"📊 Average response time: {avg_time:.3f}s over {len(times)} requests")
    
    api.close()
    return avg_time
```

## 🏢 Enterprise Integration

### CI/CD Pipeline Integration
```yaml
# .github/workflows/api-tests.yml
name: API Integration Tests
on: [push, pull_request]
jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run API tests
        run: python Free_API_Examples.py
```

### Environment Configuration
```python
import os

# Environment-based configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.default.com')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
SSL_VERIFY = os.getenv('SSL_VERIFY', 'true').lower() == 'true'

api = APITestFramework(
    base_url=API_BASE_URL,
    timeout=API_TIMEOUT,
    verify_ssl=SSL_VERIFY
)
```

## 📚 Additional Resources

### Related Documentation
- 🗄️ [Database Actions](../database_actions/README.md) - Database integration testing
- 📊 [Pandas Analysis](../pandas_analysis/README.md) - API response data analysis
- 🕷️ [Selenium Testing](../selenium%20Testing/README.md) - Web API integration testing

### External References  
- [Requests Documentation](https://docs.python-requests.org/)
- [HTTPBin Testing Service](https://httpbin.org/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)
- [REST API Best Practices](https://restfulapi.net/)

---

**🚀 Built for professional API testing and validation**

*Reliable • Comprehensive • Enterprise-Ready* ✨