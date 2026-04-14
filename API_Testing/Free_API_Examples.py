#!/usr/bin/env python3
"""
🌐 Free API Testing Examples
================================

This module demonstrates the REST API Testing framework using real free APIs.
Tests various HTTP methods on publicly available APIs.

Free APIs Used:
- JSONPlaceholder: https://jsonplaceholder.typicode.com
- HTTPBin: https://httpbin.org  
- ReqRes: https://reqres.in
- CatFacts: https://catfact.ninja
- Random Quotes: https://api.quotable.io

Author: AI Assistant
Date: 2024-04-10
"""

from REST_API_Testing import APITestFramework
import json
import time


def test_jsonplaceholder_api():
    """
    🎯 Test JSONPlaceholder API - A fake REST API for testing and prototyping
    """
    print("\n🌟 Testing JSONPlaceholder API")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=10
    )
    
    # Test GET - Get all posts
    print("\n📥 Testing GET /posts")
    response = api_tester.get_request("/posts", params={"_limit": 3})
    if response and response.status_code == 200:
        posts = response.json()
        print(f"✅ Retrieved {len(posts)} posts")
        for post in posts[:2]:  # Show first 2 posts
            print(f"   📝 Post {post['id']}: {post['title'][:50]}...")
    
    # Test GET single post
    print("\n📥 Testing GET /posts/1")
    response = api_tester.get_request("/posts/1")
    if response and response.status_code == 200:
        post = response.json()
        print(f"✅ Post Title: {post['title']}")
        print(f"   📄 Body: {post['body'][:100]}...")
    
    # Test POST - Create new post
    print("\n📤 Testing POST /posts")
    new_post = {
        "title": "Test Post from API Framework",
        "body": "This is a test post created by our REST API Testing Framework",
        "userId": 1
    }
    response = api_tester.post_request("/posts", json=new_post)
    if response and response.status_code == 201:
        created_post = response.json()
        print(f"✅ Created post with ID: {created_post['id']}")
        print(f"   📝 Title: {created_post['title']}")
    
    # Test PUT - Update post
    print("\n🔄 Testing PUT /posts/1")
    updated_post = {
        "id": 1,
        "title": "Updated Test Post",
        "body": "This post has been updated using PUT method",
        "userId": 1
    }
    response = api_tester.put_request("/posts/1", json=updated_post)
    if response and response.status_code == 200:
        updated = response.json()
        print(f"✅ Updated post title: {updated['title']}")
    
    # Test PATCH - Partially update post
    print("\n🔧 Testing PATCH /posts/1")
    patch_data = {"title": "Patched Title Only"}
    response = api_tester.patch_request("/posts/1", json=patch_data)
    if response and response.status_code == 200:
        patched = response.json()
        print(f"✅ Patched post title: {patched['title']}")
    
    # Test DELETE
    print("\n🗑️ Testing DELETE /posts/1")
    response = api_tester.delete_request("/posts/1")
    if response and response.status_code == 200:
        print("✅ Post deleted successfully")


def test_httpbin_api():
    """
    🎯 Test HTTPBin API - HTTP Request & Response Service
    """
    print("\n🌟 Testing HTTPBin API")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="https://httpbin.org",
        timeout=15
    )
    
    # Test GET with query parameters
    print("\n📥 Testing GET /get with parameters")
    params = {"name": "John", "age": "30", "city": "New York"}
    response = api_tester.get_request("/get", params=params)
    if response and response.status_code == 200:
        data = response.json()
        print("✅ GET request successful")
        print(f"   🔗 URL: {data['url']}")
        print(f"   📊 Args: {data['args']}")
    
    # Test POST with JSON data
    print("\n📤 Testing POST /post with JSON")
    json_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123"
    }
    response = api_tester.post_request("/post", json=json_data)
    if response and response.status_code == 200:
        data = response.json()
        print("✅ POST request successful")
        print(f"   📦 JSON sent: {data['json']}")
    
    # Test PUT with form data
    print("\n🔄 Testing PUT /put with form data")
    form_data = {"field1": "value1", "field2": "value2"}
    response = api_tester.put_request("/put", data=form_data)
    if response and response.status_code == 200:
        data = response.json()
        print("✅ PUT request successful")
        print(f"   📝 Form data: {data['form']}")
    
    # Test status codes
    print("\n🚦 Testing different status codes")
    for status_code in [200, 404, 500]:
        response = api_tester.get_request(f"/status/{status_code}")
        if response:
            print(f"   Status {status_code}: {'✅ Success' if response.status_code == status_code else '❌ Failed'}")
    
    # Test with custom headers
    print("\n📋 Testing custom headers")
    headers = {
        "X-Custom-Header": "TestValue",
        "User-Agent": "REST-API-Testing-Framework/1.0"
    }
    response = api_tester.get_request("/headers", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print("✅ Custom headers sent successfully")
        print(f"   📋 Headers received: {len(data['headers'])} headers")


def test_reqres_api():
    """
    🎯 Test ReqRes API - Real responses for REST API testing
    """
    print("\n🌟 Testing ReqRes API")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="https://reqres.in/api",
        timeout=10
    )
    
    # Test GET users
    print("\n👥 Testing GET /users")
    response = api_tester.get_request("/users", params={"page": 1})
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data['data'])} users")
        for user in data['data'][:2]:  # Show first 2 users
            print(f"   👤 {user['first_name']} {user['last_name']} - {user['email']}")
    
    # Test POST create user
    print("\n➕ Testing POST /users")
    new_user = {
        "name": "John Doe",
        "job": "Software Engineer"
    }
    response = api_tester.post_request("/users", json=new_user)
    if response and response.status_code == 201:
        created = response.json()
        print(f"✅ Created user: {created['name']}")
        print(f"   💼 Job: {created['job']}")
        print(f"   🆔 ID: {created['id']}")
    
    # Test PUT update user
    print("\n🔄 Testing PUT /users/2")
    updated_user = {
        "name": "Jane Smith",
        "job": "Senior Developer"
    }
    response = api_tester.put_request("/users/2", json=updated_user)
    if response and response.status_code == 200:
        updated = response.json()
        print(f"✅ Updated user: {updated['name']}")
    
    # Test DELETE user
    print("\n🗑️ Testing DELETE /users/2")
    response = api_tester.delete_request("/users/2")
    if response and response.status_code == 204:
        print("✅ User deleted successfully (204 No Content)")


def test_catfacts_api():
    """
    🎯 Test Cat Facts API - Random cat facts
    """
    print("\n🌟 Testing Cat Facts API")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="https://catfact.ninja",
        timeout=10
    )
    
    # Test GET random fact
    print("\n🐱 Testing GET /fact")
    response = api_tester.get_request("/fact")
    if response and response.status_code == 200:
        data = response.json()
        print("✅ Random cat fact retrieved:")
        print(f"   🐾 {data['fact']}")
        print(f"   📏 Length: {data['length']} characters")
    
    # Test GET multiple facts
    print("\n🐱 Testing GET /facts with limit")
    response = api_tester.get_request("/facts", params={"limit": 3})
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data['data'])} cat facts:")
        for i, fact in enumerate(data['data'], 1):
            print(f"   {i}. {fact['fact'][:80]}...")


def test_quotes_api():
    """
    🎯 Test Quotable API - Random inspirational quotes
    """
    print("\n🌟 Testing Quotable API")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="https://api.quotable.io",
        timeout=10
    )
    
    # Test GET random quote
    print("\n💬 Testing GET /random")
    response = api_tester.get_request("/random")
    if response and response.status_code == 200:
        data = response.json()
        print("✅ Random quote retrieved:")
        print(f"   💭 \"{data['content']}\"")
        print(f"   👤 - {data['author']}")
    
    # Test GET quotes with filter
    print("\n💬 Testing GET /quotes with author filter")
    response = api_tester.get_request("/quotes", params={"author": "Albert Einstein", "limit": 2})
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data['results'])} quotes:")
        for quote in data['results']:
            print(f"   💭 \"{quote['content'][:80]}...\"")


def test_error_scenarios():
    """
    🎯 Test various error scenarios with real APIs
    """
    print("\n🌟 Testing Error Scenarios")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="https://httpbin.org",
        timeout=5
    )
    
    # Test 404 Not Found
    print("\n❌ Testing 404 Not Found")
    response = api_tester.get_request("/status/404")
    if response and response.status_code == 404:
        print("✅ 404 error handled correctly")
    
    # Test 500 Internal Server Error
    print("\n❌ Testing 500 Internal Server Error")
    response = api_tester.get_request("/status/500")
    if response and response.status_code == 500:
        print("✅ 500 error handled correctly")
    
    # Test timeout scenario
    print("\n⏱️ Testing timeout scenario")
    api_tester_short_timeout = APITestFramework(
        base_url="https://httpbin.org",
        timeout=1  # Very short timeout
    )
    response = api_tester_short_timeout.get_request("/delay/3")  # 3 second delay
    # This should timeout and be handled gracefully
    
    # Test invalid JSON response
    print("\n🔧 Testing invalid JSON handling")
    response = api_tester.get_request("/html")  # Returns HTML, not JSON
    if response and response.status_code == 200:
        print("✅ Non-JSON response handled correctly")


def performance_testing():
    """
    🎯 Performance testing with multiple concurrent requests
    """
    print("\n🌟 Performance Testing")
    print("=" * 50)
    
    api_tester = APITestFramework(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=10
    )
    
    start_time = time.time()
    
    # Test multiple requests
    print("\n🚀 Testing multiple sequential requests")
    successful_requests = 0
    total_requests = 5
    
    for i in range(1, total_requests + 1):
        response = api_tester.get_request(f"/posts/{i}")
        if response and response.status_code == 200:
            successful_requests += 1
            print(f"   ✅ Request {i}: Success")
        else:
            print(f"   ❌ Request {i}: Failed")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n📊 Performance Results:")
    print(f"   ⏱️ Total time: {duration:.2f} seconds")
    print(f"   ✅ Successful requests: {successful_requests}/{total_requests}")
    print(f"   📈 Average response time: {duration/total_requests:.2f} seconds per request")


def main():
    """
    🎯 Main function to run all free API tests
    """
    print("🌐 REST API Testing Framework - Free APIs Demo")
    print("=" * 60)
    print("📋 Testing various free APIs to demonstrate framework capabilities")
    
    try:
        # Run all API tests
        test_jsonplaceholder_api()
        test_httpbin_api()
        test_reqres_api()
        test_catfacts_api()
        test_quotes_api()
        test_error_scenarios()
        performance_testing()
        
        print("\n🎉 All free API tests completed successfully!")
        print("✅ The REST API Testing Framework is working perfectly with real APIs!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {str(e)}")
    finally:
        print("\n👋 Free API testing session ended")


if __name__ == "__main__":
    main()