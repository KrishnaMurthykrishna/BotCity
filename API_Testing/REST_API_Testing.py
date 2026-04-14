# -*- coding: utf-8 -*-
"""
REST API Testing Framework

This module provides comprehensive REST API testing functionality with support for:
- GET, POST, PUT, PATCH, DELETE HTTP methods
- Parameter handling and validation
- Error scenarios and comprehensive error handling
- Response validation and logging

Author: Automated Testing Framework
Created: April 10, 2026
Last Modified: April 10, 2026
"""

import requests
import json
import logging
import os
import sys
import time
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin, urlparse
import random
import string


def setup_logging(script_name: str = "REST_API_Testing") -> logging.Logger:
    """
    Setup comprehensive logging configuration with both file and console handlers.
    
    Args:
        script_name (str): Name prefix for the log file
    
    Returns:
        logging.Logger: Configured logger instance
    """
    try:
        # Create logs directory if it doesn't exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(script_dir, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"📁 Created logs directory: {log_dir}")

        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(log_dir, f'{script_name}_{timestamp}.log')

        # Configure root logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )

        logger = logging.getLogger(__name__)
        logger.info(f"🚀 API Testing logging initialized successfully - Log file: {log_filename}")
        print(f"🚀 API Testing logging initialized successfully - Log file: {log_filename}")
        return logger

    except Exception as e:
        print(f"❌ Failed to setup logging: {str(e)}")
        # Fallback to basic logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)


# Initialize logging
logger = setup_logging("REST_API_Testing")


class APITestFramework:
    """
    Comprehensive REST API testing framework.
    
    This class provides methods for testing various HTTP operations with:
    - Comprehensive error handling and logging
    - Response validation and analysis
    - Test scenario generation
    - Error injection for negative testing
    
    Attributes:
        base_url: Base URL for API endpoints
        session: Requests session for connection pooling
        timeout: Default timeout for requests
        logger: Logger instance for this class
    """
    
    def __init__(self, base_url: str = "", timeout: int = 30, headers: Optional[Dict[str, str]] = None, verify_ssl: bool = True):
        """
        Initialize the API testing framework.
        
        Args:
            base_url (str): Base URL for API endpoints
            timeout (int): Default timeout for requests in seconds
            headers (Dict[str, str], optional): Default headers for requests
            verify_ssl (bool): Whether to verify SSL certificates (default: True)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Disable SSL warnings if verification is disabled
        if not verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Set default headers
        default_headers = {
            'User-Agent': 'REST-API-Testing-Framework/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        if headers:
            default_headers.update(headers)
            
        self.session.headers.update(default_headers)
        
        self.logger.info("🏗️ API Testing Framework initialized")
        self.logger.info(f"🌐 Base URL: {self.base_url}")
        self.logger.info(f"⏱️ Timeout: {timeout}s")
        self.logger.info(f"🔒 SSL Verification: {'Enabled' if verify_ssl else 'Disabled'}")
        print("🏗️ API Testing Framework initialized")

    def _validate_url(self, endpoint: str) -> str:
        """
        Validate and construct full URL from endpoint.
        
        Args:
            endpoint (str): API endpoint
            
        Returns:
            str: Full URL
        """
        if endpoint.startswith(('http://', 'https://')):
            return endpoint
        
        if self.base_url:
            return urljoin(self.base_url + '/', endpoint.lstrip('/'))
        
        raise ValueError("❌ No base URL configured and endpoint is not absolute")

    def _log_request(self, method: str, url: str, **kwargs):
        """Log request details."""
        self.logger.info(f"📤 {method.upper()} Request: {url}")
        
        if 'params' in kwargs and kwargs['params']:
            self.logger.info(f"🔗 Query Parameters: {kwargs['params']}")
            
        if 'json' in kwargs and kwargs['json']:
            self.logger.info(f"📋 Request Body: {json.dumps(kwargs['json'], indent=2)}")
            
        if 'data' in kwargs and kwargs['data']:
            self.logger.info(f"📄 Form Data: {kwargs['data']}")

    def _log_response(self, response: requests.Response):
        """Log response details."""
        self.logger.info(f"📥 Response Status: {response.status_code} {response.reason}")
        self.logger.info(f"⏱️ Response Time: {response.elapsed.total_seconds():.3f}s")
        self.logger.info(f"📏 Response Size: {len(response.content)} bytes")
        
        # Log response headers (filtered for security)
        safe_headers = {k: v for k, v in response.headers.items() 
                       if not any(sensitive in k.lower() for sensitive in ['auth', 'token', 'key'])}
        self.logger.info(f"📋 Response Headers: {dict(safe_headers)}")

    def get_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                   headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform GET request with comprehensive error handling.
        
        Args:
            endpoint (str): API endpoint
            params (Dict[str, Any], optional): Query parameters
            headers (Dict[str, str], optional): Additional headers
            **kwargs: Additional request parameters
            
        Returns:
            Dict[str, Any]: Response data with metadata
        """
        try:
            url = self._validate_url(endpoint)
            self.logger.info(f"🔍 Starting GET request to: {endpoint}")
            
            # Merge headers
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            # Log request details
            request_kwargs = {
                'params': params,
                'headers': request_headers,
                'timeout': self.timeout,                'verify': self.verify_ssl,                'verify': self.verify_ssl,
                **kwargs
            }
            self._log_request('GET', url, **request_kwargs)
            
            # Make request
            start_time = time.time()
            response = self.session.get(url, **request_kwargs)
            duration = time.time() - start_time
            
            # Log response
            self._log_response(response)
            
            # Parse response
            result = self._parse_response(response, duration)
            
            self.logger.info("✅ GET request completed successfully")
            print(f"✅ GET {endpoint} - Status: {response.status_code}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ GET request failed for {endpoint}: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            print(error_msg)
            
            return {
                'success': False,
                'error': str(e),
                'status_code': None,
                'endpoint': endpoint,
                'method': 'GET'
            }

    def post_request(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                    json_data: Optional[Dict[str, Any]] = None, 
                    params: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform POST request with comprehensive error handling.
        
        Args:
            endpoint (str): API endpoint
            data (Dict[str, Any], optional): Form data
            json_data (Dict[str, Any], optional): JSON data
            params (Dict[str, Any], optional): Query parameters
            headers (Dict[str, str], optional): Additional headers
            **kwargs: Additional request parameters
            
        Returns:
            Dict[str, Any]: Response data with metadata
        """
        try:
            url = self._validate_url(endpoint)
            self.logger.info(f"📝 Starting POST request to: {endpoint}")
            
            # Merge headers
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            # Prepare request data
            request_kwargs = {
                'params': params,
                'headers': request_headers,
                'timeout': self.timeout,
                **kwargs
            }
            
            if json_data:
                request_kwargs['json'] = json_data
            elif data:
                request_kwargs['data'] = data
            
            # Log request details
            self._log_request('POST', url, **request_kwargs)
            
            # Make request
            start_time = time.time()
            response = self.session.post(url, **request_kwargs)
            duration = time.time() - start_time
            
            # Log response
            self._log_response(response)
            
            # Parse response
            result = self._parse_response(response, duration)
            
            self.logger.info("✅ POST request completed successfully")
            print(f"✅ POST {endpoint} - Status: {response.status_code}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ POST request failed for {endpoint}: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            print(error_msg)
            
            return {
                'success': False,
                'error': str(e),
                'status_code': None,
                'endpoint': endpoint,
                'method': 'POST'
            }

    def put_request(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                   json_data: Optional[Dict[str, Any]] = None,
                   params: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform PUT request with comprehensive error handling.
        
        Args:
            endpoint (str): API endpoint
            data (Dict[str, Any], optional): Form data
            json_data (Dict[str, Any], optional): JSON data
            params (Dict[str, Any], optional): Query parameters
            headers (Dict[str, str], optional): Additional headers
            **kwargs: Additional request parameters
            
        Returns:
            Dict[str, Any]: Response data with metadata
        """
        try:
            url = self._validate_url(endpoint)
            self.logger.info(f"🔄 Starting PUT request to: {endpoint}")
            
            # Merge headers
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            # Prepare request data
            request_kwargs = {
                'params': params,
                'headers': request_headers,
                'timeout': self.timeout,
                **kwargs
            }
            
            if json_data:
                request_kwargs['json'] = json_data
            elif data:
                request_kwargs['data'] = data
            
            # Log request details
            self._log_request('PUT', url, **request_kwargs)
            
            # Make request
            start_time = time.time()
            response = self.session.put(url, **request_kwargs)
            duration = time.time() - start_time
            
            # Log response
            self._log_response(response)
            
            # Parse response
            result = self._parse_response(response, duration)
            
            self.logger.info("✅ PUT request completed successfully")
            print(f"✅ PUT {endpoint} - Status: {response.status_code}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ PUT request failed for {endpoint}: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            print(error_msg)
            
            return {
                'success': False,
                'error': str(e),
                'status_code': None,
                'endpoint': endpoint,
                'method': 'PUT'
            }

    def patch_request(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                     json_data: Optional[Dict[str, Any]] = None,
                     params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform PATCH request with comprehensive error handling.
        
        Args:
            endpoint (str): API endpoint
            data (Dict[str, Any], optional): Form data
            json_data (Dict[str, Any], optional): JSON data
            params (Dict[str, Any], optional): Query parameters
            headers (Dict[str, str], optional): Additional headers
            **kwargs: Additional request parameters
            
        Returns:
            Dict[str, Any]: Response data with metadata
        """
        try:
            url = self._validate_url(endpoint)
            self.logger.info(f"🔧 Starting PATCH request to: {endpoint}")
            
            # Merge headers
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            # Prepare request data
            request_kwargs = {
                'params': params,
                'headers': request_headers,
                'timeout': self.timeout,
                **kwargs
            }
            
            if json_data:
                request_kwargs['json'] = json_data
            elif data:
                request_kwargs['data'] = data
            
            # Log request details
            self._log_request('PATCH', url, **request_kwargs)
            
            # Make request
            start_time = time.time()
            response = self.session.patch(url, **request_kwargs)
            duration = time.time() - start_time
            
            # Log response
            self._log_response(response)
            
            # Parse response
            result = self._parse_response(response, duration)
            
            self.logger.info("✅ PATCH request completed successfully")
            print(f"✅ PATCH {endpoint} - Status: {response.status_code}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ PATCH request failed for {endpoint}: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            print(error_msg)
            
            return {
                'success': False,
                'error': str(e),
                'status_code': None,
                'endpoint': endpoint,
                'method': 'PATCH'
            }

    def delete_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                      headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform DELETE request with comprehensive error handling.
        
        Args:
            endpoint (str): API endpoint
            params (Dict[str, Any], optional): Query parameters
            headers (Dict[str, str], optional): Additional headers
            **kwargs: Additional request parameters
            
        Returns:
            Dict[str, Any]: Response data with metadata
        """
        try:
            url = self._validate_url(endpoint)
            self.logger.info(f"🗑️ Starting DELETE request to: {endpoint}")
            
            # Merge headers
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            # Prepare request
            request_kwargs = {
                'params': params,
                'headers': request_headers,
                'timeout': self.timeout,
                **kwargs
            }
            
            # Log request details
            self._log_request('DELETE', url, **request_kwargs)
            
            # Make request
            start_time = time.time()
            response = self.session.delete(url, **request_kwargs)
            duration = time.time() - start_time
            
            # Log response
            self._log_response(response)
            
            # Parse response
            result = self._parse_response(response, duration)
            
            self.logger.info("✅ DELETE request completed successfully")
            print(f"✅ DELETE {endpoint} - Status: {response.status_code}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ DELETE request failed for {endpoint}: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            print(error_msg)
            
            return {
                'success': False,
                'error': str(e),
                'status_code': None,
                'endpoint': endpoint,
                'method': 'DELETE'
            }

    def _parse_response(self, response: requests.Response, duration: float) -> Dict[str, Any]:
        """
        Parse and structure response data.
        
        Args:
            response (requests.Response): HTTP response object
            duration (float): Request duration in seconds
            
        Returns:
            Dict[str, Any]: Structured response data
        """
        result = {
            'success': response.ok,
            'status_code': response.status_code,
            'reason': response.reason,
            'duration': round(duration, 3),
            'size': len(response.content),
            'headers': dict(response.headers),
            'url': response.url,
            'encoding': response.encoding
        }
        
        # Try to parse JSON response
        try:
            if response.headers.get('content-type', '').startswith('application/json'):
                result['json'] = response.json()
            else:
                result['text'] = response.text
        except json.JSONDecodeError:
            result['text'] = response.text
            self.logger.warning("⚠️ Failed to parse JSON response")
        
        return result

    def generate_test_error(self, error_type: str = "random") -> Dict[str, Any]:
        """
        Generate intentional errors for testing error handling.
        
        This function creates various error scenarios to test error handling:
        - Network timeouts
        - Invalid URLs
        - Invalid JSON
        - Connection errors
        - HTTP errors
        
        Args:
            error_type (str): Type of error to generate
                Options: "timeout", "invalid_url", "invalid_json", 
                        "connection", "http_error", "random"
            
        Returns:
            Dict[str, Any]: Error response data
        """
        try:
            self.logger.info(f"🎯 Generating test error: {error_type}")
            print(f"🎯 Generating test error: {error_type}")
            
            if error_type == "random":
                error_type = random.choice([
                    "timeout", "invalid_url", "invalid_json", 
                    "connection", "http_error"
                ])
            
            if error_type == "timeout":
                # Generate timeout error
                self.logger.info("⏰ Testing timeout error...")
                return self.get_request("https://httpbin.org/delay/35", timeout=5)
            
            elif error_type == "invalid_url":
                # Generate invalid URL error
                self.logger.info("🔗 Testing invalid URL error...")
                return self.get_request("not-a-valid-url://invalid")
            
            elif error_type == "invalid_json":
                # Generate invalid JSON error by sending malformed data
                self.logger.info("📋 Testing invalid JSON error...")
                malformed_data = '{"invalid": json, "missing": quote}'
                try:
                    json.loads(malformed_data)  # This will raise JSONDecodeError
                except json.JSONDecodeError as e:
                    return {
                        'success': False,
                        'error': f"JSON Decode Error: {str(e)}",
                        'error_type': 'invalid_json',
                        'method': 'TEST_ERROR'
                    }
            
            elif error_type == "connection":
                # Generate connection error
                self.logger.info("🌐 Testing connection error...")
                return self.get_request("http://non-existent-domain-12345.com")
            
            elif error_type == "http_error":
                # Generate HTTP error (404, 500, etc.)
                self.logger.info("❌ Testing HTTP error...")
                return self.get_request("https://httpbin.org/status/500")
            
            else:
                raise ValueError(f"Unknown error type: {error_type}")
                
        except Exception as e:
            error_msg = f"❌ Error generation failed: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            print(error_msg)
            
            return {
                'success': False,
                'error': str(e),
                'error_type': error_type,
                'method': 'ERROR_GENERATION'
            }

    def run_test_scenarios(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Run comprehensive test scenarios covering various API operations.
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: Test results organized by category
        """
        self.logger.info("🧪 Starting comprehensive API test scenarios...")
        print("="*60)
        print("🧪 Starting Comprehensive API Test Scenarios")
        print("="*60)
        
        results = {
            'get_tests': [],
            'post_tests': [],
            'put_tests': [],
            'patch_tests': [],
            'delete_tests': [],
            'error_tests': []
        }
        
        try:
            # GET Tests
            print("\n🔍 Running GET Tests...")
            results['get_tests'].extend([
                self.get_request("https://httpbin.org/get"),
                self.get_request("https://httpbin.org/json"),
                self.get_request("https://httpbin.org/get", params={'test': 'value', 'number': 123})
            ])
            
            # POST Tests
            print("\n📝 Running POST Tests...")
            results['post_tests'].extend([
                self.post_request("https://httpbin.org/post", json_data={'test': 'data', 'timestamp': str(datetime.now())}),
                self.post_request("https://httpbin.org/post", data={'form_field': 'form_value'}),
                self.post_request("https://httpbin.org/post", json_data={'id': 1, 'name': 'Test User', 'active': True})
            ])
            
            # PUT Tests
            print("\n🔄 Running PUT Tests...")
            results['put_tests'].extend([
                self.put_request("https://httpbin.org/put", json_data={'id': 1, 'updated': True}),
                self.put_request("https://httpbin.org/put", json_data={'resource': 'updated', 'version': 2})
            ])
            
            # PATCH Tests
            print("\n🔧 Running PATCH Tests...")
            results['patch_tests'].extend([
                self.patch_request("https://httpbin.org/patch", json_data={'field': 'partial_update'}),
                self.patch_request("https://httpbin.org/patch", json_data={'status': 'active'})
            ])
            
            # DELETE Tests
            print("\n🗑️ Running DELETE Tests...")
            results['delete_tests'].extend([
                self.delete_request("https://httpbin.org/delete"),
                self.delete_request("https://httpbin.org/delete", params={'id': '123'})
            ])
            
            # Error Tests
            print("\n❌ Running Error Tests...")
            results['error_tests'].extend([
                self.generate_test_error("timeout"),
                self.generate_test_error("invalid_url"),
                self.generate_test_error("invalid_json"),
                self.generate_test_error("connection"),
                self.generate_test_error("http_error")
            ])
            
            # Summary
            self._print_test_summary(results)
            
            self.logger.info("✅ All test scenarios completed")
            print("\n✅ All test scenarios completed successfully")
            
            return results
            
        except Exception as e:
            error_msg = f"❌ Test scenarios failed: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            print(error_msg)
            
            return results

    def _print_test_summary(self, results: Dict[str, List[Dict[str, Any]]]):
        """Print test results summary."""
        print("\n📊 Test Results Summary")
        print("="*40)
        
        total_tests = 0
        passed_tests = 0
        
        for category, tests in results.items():
            category_passed = sum(1 for test in tests if test.get('success', False))
            category_total = len(tests)
            
            total_tests += category_total
            passed_tests += category_passed
            
            status = "✅" if category_passed == category_total else "❌"
            print(f"{status} {category.replace('_', ' ').title()}: {category_passed}/{category_total}")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"\n📈 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")

    def close(self):
        """Clean up resources."""
        try:
            self.session.close()
            self.logger.info("🧹 API Testing Framework resources cleaned up")
            print("🧹 Resources cleaned up successfully")
        except Exception as e:
            self.logger.warning(f"⚠️ Cleanup warning: {str(e)}")


def main():
    """
    Main execution function demonstrating API testing framework usage.
    """
    try:
        print("🚀 Starting REST API Testing Framework")
        print("="*60)
        
        # Initialize framework
        api_tester = APITestFramework(
            base_url="https://httpbin.org",
            timeout=30,
            headers={'X-Test-Framework': 'REST-API-Testing'}
        )
        
        # Run individual tests
        print("\n🎯 Running Individual API Tests...")
        
        # GET test
        get_result = api_tester.get_request("/get", params={'demo': 'test'})
        
        # POST test
        post_result = api_tester.post_request("/post", json_data={
            'user': 'tester',
            'action': 'demo',
            'timestamp': datetime.now().isoformat()
        })
        
        # PUT test
        put_result = api_tester.put_request("/put", json_data={
            'resource_id': 123,
            'update_type': 'full'
        })
        
        # Error generation test
        print("\n💥 Testing Error Generation...")
        error_result = api_tester.generate_test_error("random")
        
        # Run comprehensive test scenarios
        print("\n🧪 Running Comprehensive Test Suite...")
        test_results = api_tester.run_test_scenarios()
        
        # Save results to file
        results_file = f"api_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(test_results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {results_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Main execution failed: {str(e)}")
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        print(f"❌ Main execution failed: {str(e)}")
        return False
        
    finally:
        # Cleanup
        try:
            api_tester.close()
        except:
            pass


if __name__ == "__main__":
    """
    Main entry point for the REST API Testing Framework.
    
    This script demonstrates comprehensive REST API testing including:
    - GET, POST, PUT, PATCH, DELETE operations
    - Parameter handling and validation
    - Error scenarios and error handling
    - Response analysis and logging
    """
    
    success = main()
    
    if success:
        print("\n" + "="*60)
        print("🎉 REST API Testing Framework completed successfully!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ REST API Testing Framework encountered errors!")
        print("="*60)
        sys.exit(1)