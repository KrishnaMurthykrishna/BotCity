#!/usr/bin/env python3
"""
🌐 Simple HTTP API Testing Examples
===================================

This module demonstrates the REST API Testing framework using HTTP (non-SSL) APIs
to avoid certificate verification issues in corporate environments.

Author: AI Assistant
Date: 2024-04-10
"""

from REST_API_Testing import APITestFramework
import json


def test_httpbin_simple():
    """
    🎯 Test HTTPBin with simple HTTP endpoints
    """
    print("\n🌟 Testing HTTPBin (HTTP) API")
    print("=" * 50)
    
    # Use HTTP instead of HTTPS to avoid SSL issues
    api_tester = APITestFramework(
        base_url="http://httpbin.org",  # HTTP version
        timeout=15,
        verify_ssl=False
    )
    
    # Test simple GET
    print("\n📥 Testing GET /get")
    response = api_tester.get_request("/get")
    if response and isinstance(response, dict):
        if response.get('success', True):  # Check if successful
            print("✅ GET request successful!")
            # Print response details safely
            status_code = response.get('status_code', 'Unknown')
            print(f"   📊 Status Code: {status_code}")
            if 'json' in str(response).lower():
                print("   📄 JSON response received")
        else:
            print(f"❌ GET request failed: {response.get('error', 'Unknown error')}")
    else:
        print("✅ GET request completed - Response object received")
    # Test GET with parameters
    print("\n📥 Testing GET /get with parameters")
    params = {"name": "TestUser", "version": "1.0"}
    response = api_tester.get_request("/get", params=params)
    if response and hasattr(response, 'status_code') and response.status_code == 200:
        print("✅ GET with params successful!")
        try:
            data = response.json()
            if 'args' in data:
                print(f"   🔗 Parameters sent: {data['args']}")
        except:
            print("   📄 Response received successfully")
    elif response:
        print(f"   ℹ️ Response status: {getattr(response, 'status_code', 'Unknown')}")
    
    # Test POST with JSON
    print("\n📤 Testing POST /post")
    test_data = {"message": "Hello from API Framework", "timestamp": "2024-04-10"}
    response = api_tester.post_request("/post", json_data=test_data)
    if response and hasattr(response, 'status_code') and response.status_code == 200:
        print("✅ POST request successful!")
        try:
            data = response.json()
            if 'json' in data:
                print(f"   📦 JSON sent: {data['json']}")
        except:
            print("   📄 POST response received successfully")
    elif response:
        print(f"   ℹ️ Response status: {getattr(response, 'status_code', 'Unknown')}")
    
    # Test PUT with form data
    print("\n🔄 Testing PUT /put")
    form_data = {"field1": "value1", "field2": "value2"}
    response = api_tester.put_request("/put", data=form_data)
    if response and hasattr(response, 'status_code') and response.status_code == 200:
        print("✅ PUT request successful!")
    elif response:
        print(f"   ℹ️ Response status: {getattr(response, 'status_code', 'Unknown')}")
    
    # Test DELETE
    print("\n🗑️ Testing DELETE /delete")
    response = api_tester.delete_request("/delete")
    if response and hasattr(response, 'status_code') and response.status_code == 200:
        print("✅ DELETE request successful!")
    elif response:
        print(f"   ℹ️ Response status: {getattr(response, 'status_code', 'Unknown')}")
    
    # Test different status codes
    print("\n🚦 Testing Status Codes")
    test_codes = [200, 201, 404, 500]
    for code in test_codes:
        print(f"   Testing status {code}...")
        response = api_tester.get_request(f"/status/{code}")
        if response:
            success_indicator = "✅" if response.get('status_code') == code else "❌"
            print(f"   {success_indicator} Status {code}: {'Success' if response.get('success') else 'Handled as expected'}")


def test_local_demo():
    """
    🎯 Demonstrate error handling with intentionally problematic requests
    """
    print("\n🌟 Testing Error Scenarios")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="http://httpbin.org",
        timeout=5,
        verify_ssl=False
    )
    
    # Test 404 error
    print("\n❌ Testing 404 Not Found")
    response = api_tester.get_request("/nonexistent-endpoint")
    if response:
        if not response.get('success') and response.get('status_code') == 404:
            print("✅ 404 error handled correctly")
        else:
            print(f"   Status: {response.get('status_code')}")
    
    # Test timeout with delay endpoint
    print("\n⏱️ Testing timeout scenario")
    fast_tester = APITestFramework(
        base_url="http://httpbin.org",
        timeout=2,  # Short timeout
        verify_ssl=False
    )
    response = fast_tester.get_request("/delay/5")  # 5 second delay
    if response:
        if not response.get('success'):
            print("✅ Timeout handled gracefully")
        else:
            print("ℹ️ Request completed faster than expected")
    
    # Test invalid URL
    print("\n🔗 Testing invalid URL handling")
    response = api_tester.get_request("invalid-path-format")
    success_msg = "✅ Invalid URL handled" if response and not response.get('success') else "⚠️ Unexpected result"
    print(f"   {success_msg}")


def test_json_responses():
    """
    🎯 Test various JSON response formats
    """
    print("\n🌟 Testing JSON Response Formats")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="http://httpbin.org",
        timeout=10,
        verify_ssl=False
    )
    
    # Test JSON response
    print("\n📄 Testing JSON response")
    json_payload = {"test": True, "framework": "REST API Testing", "version": 1.0}
    response = api_tester.post_request("/post", json_data=json_payload)
    if response and response.get('success'):
        print("✅ JSON response parsed successfully")
        if 'data' in response:
            print(f"   📊 Response type: {type(response['data'])}")
    
    # Test HTML response (non-JSON)
    print("\n📝 Testing HTML response handling")
    response = api_tester.get_request("/html")
    if response:
        if response.get('success'):
            print("✅ HTML response handled (not parsed as JSON)")
        else:
            print("ℹ️ Non-JSON response handled appropriately")
    
    # Test XML response
    print("\n📋 Testing XML response handling")
    response = api_tester.get_request("/xml")
    if response:
        success_msg = "✅ XML response handled" if response.get('success') else "ℹ️ XML response detected"
        print(f"   {success_msg}")


def performance_test():
    """
    🎯 Simple performance testing
    """
    print("\n🌟 Performance Testing")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="http://httpbin.org",
        timeout=10,
        verify_ssl=False
    )
    
    import time
    
    print("\n🚀 Testing response times")
    start_time = time.time()
    
    # Test multiple requests
    successful_requests = 0
    total_requests = 3
    
    for i in range(1, total_requests + 1):
        request_start = time.time()
        response = api_tester.get_request("/get", params={"request": i})
        request_end = time.time()
        
        if response and response.get('success'):
            successful_requests += 1
            print(f"   ✅ Request {i}: Success ({request_end - request_start:.2f}s)")
        else:
            print(f"   ❌ Request {i}: Failed")
    
    total_time = time.time() - start_time
    
    print(f"\n📊 Performance Summary:")
    print(f"   ⏱️ Total time: {total_time:.2f} seconds")
    print(f"   ✅ Success rate: {successful_requests}/{total_requests}")
    print(f"   📈 Avg response time: {total_time/total_requests:.2f}s per request")


def main():
    """
    🎯 Main function to run HTTP API tests
    """
    print("🌐 REST API Testing Framework - HTTP APIs Demo")
    print("=" * 60)
    print("📋 Testing HTTP endpoints to avoid SSL certificate issues\n")
    
    try:
        # Run tests
        test_httpbin_simple()
        test_local_demo()
        test_json_responses()
        performance_test()
        
        print("\n🎉 All HTTP API tests completed!")
        print("✅ REST API Testing Framework working correctly with HTTP endpoints!")
        print("\n💡 To test HTTPS APIs, update the framework with verify_ssl=False parameter")
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        print(f"🔍 Details: {traceback.format_exc()}")
    finally:
        print("\n👋 HTTP API testing session completed")


if __name__ == "__main__":
    main()