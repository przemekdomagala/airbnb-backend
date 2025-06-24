#!/usr/bin/env python
"""
Test script for the Admin API
Run this after starting the Django server to test the admin user management API.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_api():
    print("🧪 Testing Admin API Endpoints")
    print("=" * 50)
    
    # First, login as admin to get token
    print("1. Logging in as admin...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@test.com",
        "password": "testpass123"
    })
    
    if login_response.status_code != 200:
        print("❌ Failed to login as admin. Make sure the test admin user exists.")
        print(f"Response: {login_response.text}")
        return
    
    admin_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print("✅ Successfully logged in as admin")
    
    # Test 0: Verify system has users
    print("\n1b. Verifying system has users...")
    initial_stats = requests.get(f"{BASE_URL}/api/admin/users/stats/", headers=headers)
    
    if initial_stats.status_code == 200:
        stats = initial_stats.json()
        total_users = stats['total_users']
        if total_users > 0:
            print(f"✅ System has {total_users} users - proceeding with tests")
        else:
            print("⚠️  System has no users - some tests may behave differently")
    else:
        print("❌ Could not verify initial user count")
    
    # Test 1: Get user statistics
    print("\n2. Getting user statistics...")
    stats_response = requests.get(f"{BASE_URL}/api/admin/users/stats/", headers=headers)
    
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print("✅ User statistics retrieved:")
        print(f"   Total users: {stats['total_users']}")
        print(f"   Active users: {stats['active_users']}")
        print(f"   Role distribution: {stats['role_distribution']}")
    else:
        print(f"❌ Failed to get stats: {stats_response.status_code}")
        print(f"Response: {stats_response.text}")
    
    # Test 2: List users
    print("\n3. Listing users...")
    users_response = requests.get(f"{BASE_URL}/api/admin/users/", headers=headers)
    
    if users_response.status_code == 200:
        users_data = users_response.json()
        # Handle both paginated and non-paginated responses
        if isinstance(users_data, dict) and 'count' in users_data:
            # Paginated response
            user_count = users_data['count']
            print(f"✅ Retrieved {user_count} users")
            if user_count > 0:
                if users_data['results']:
                    first_user = users_data['results'][0]
                    print(f"   First user: {first_user['username']} ({first_user['email']})")
                    print(f"   Users per page: {len(users_data['results'])}")
                else:
                    print("   ⚠️  User count > 0 but no results returned")
            else:
                print("   ℹ️  No users found in the system")
        elif isinstance(users_data, list):
            # Non-paginated response
            user_count = len(users_data)
            print(f"✅ Retrieved {user_count} users")
            if user_count > 0:
                first_user = users_data[0]
                print(f"   First user: {first_user['username']} ({first_user['email']})")
            else:
                print("   ℹ️  No users found in the system")
        else:
            print(f"✅ Retrieved users data: {type(users_data)}")
    else:
        print(f"❌ Failed to list users: {users_response.status_code}")
        print(f"Response: {users_response.text}")
    
    # Test 2b: Test search functionality
    print("\n3b. Testing user search...")
    search_response = requests.get(f"{BASE_URL}/api/admin/users/?search=admin", headers=headers)
    
    if search_response.status_code == 200:
        search_data = search_response.json()
        if isinstance(search_data, dict) and 'count' in search_data:
            print(f"✅ Search returned {search_data['count']} users matching 'admin'")
        elif isinstance(search_data, list):
            print(f"✅ Search returned {len(search_data)} users matching 'admin'")
    else:
        print(f"❌ Failed to search users: {search_response.status_code}")
    
    # Test 2c: Test pagination
    print("\n3c. Testing pagination...")
    page_response = requests.get(f"{BASE_URL}/api/admin/users/?page_size=5&page=1", headers=headers)
    
    if page_response.status_code == 200:
        page_data = page_response.json()
        if isinstance(page_data, dict) and 'count' in page_data:
            total_users = page_data['count']
            returned_users = len(page_data['results']) if page_data['results'] else 0
            print(f"✅ Pagination working: {returned_users} users returned from {total_users} total")
            if page_data.get('next'):
                print("   ✅ Next page available")
            if page_data.get('previous'):
                print("   ✅ Previous page available")
        else:
            print(f"✅ Pagination response: {len(page_data)} users")
    else:
        print(f"❌ Failed to test pagination: {page_response.status_code}")
    
    # Test 3: Create a new user
    print("\n4. Creating a new test user...")
    import time
    timestamp = str(int(time.time()))
    new_user_data = {
        "username": f"testuser_admin_api_{timestamp}",
        "email": f"testuser_admin_{timestamp}@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "role": "guest"
    }
    
    create_response = requests.post(f"{BASE_URL}/api/admin/users/", 
                                  json=new_user_data, headers=headers)
    
    if create_response.status_code == 201:
        new_user = create_response.json()
        user_id = new_user.get('id')
        if user_id:
            print(f"✅ Created user: {new_user['username']} (ID: {user_id})")
        else:
            print(f"❌ User created but no ID in response: {new_user}")
            return
        
        # Test 4: Change user role
        print(f"\n5. Changing user role to landlord...")
        role_response = requests.post(f"{BASE_URL}/api/admin/users/{user_id}/change_role/",
                                    json={"role": "landlord"}, headers=headers)
        
        if role_response.status_code == 200:
            print("✅ Successfully changed user role to landlord")
        else:
            print(f"❌ Failed to change role: {role_response.status_code}")
        
        # Test 5: Deactivate user
        print(f"\n6. Deactivating user...")
        deactivate_response = requests.post(f"{BASE_URL}/api/admin/users/{user_id}/deactivate/",
                                          headers=headers)
        
        if deactivate_response.status_code == 200:
            print("✅ Successfully deactivated user")
        else:
            print(f"❌ Failed to deactivate user: {deactivate_response.status_code}")
        
        # Test 6: Delete user (cleanup)
        print(f"\n7. Cleaning up - deleting test user...")
        delete_response = requests.delete(f"{BASE_URL}/api/admin/users/{user_id}/",
                                        headers=headers)
        
        if delete_response.status_code == 204:
            print("✅ Successfully deleted test user")
        else:
            print(f"❌ Failed to delete user: {delete_response.status_code}")
            
    else:
        print(f"❌ Failed to create user: {create_response.status_code}")
        print(f"Response: {create_response.text}")
    
    # Test 7: Test access control (try with guest user)
    print("\n8. Testing access control with guest user...")
    guest_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "guest@test.com",
        "password": "testpass123"
    })
    
    if guest_login.status_code == 200:
        guest_token = guest_login.json()["access_token"]
        guest_headers = {"Authorization": f"Bearer {guest_token}"}
        
        # Try to access admin endpoint
        forbidden_response = requests.get(f"{BASE_URL}/api/admin/users/stats/", 
                                        headers=guest_headers)
        
        if forbidden_response.status_code == 403:
            print("✅ Access control working - guest user correctly denied")
        else:
            print(f"❌ Access control issue: {forbidden_response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 Admin API testing completed!")

if __name__ == "__main__":
    test_admin_api()
