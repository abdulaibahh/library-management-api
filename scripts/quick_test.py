import requests

# Test health
r = requests.get('http://127.0.0.1:8000/health')
print(f'Health: {r.status_code} - {r.text}\n')

# Register
data = {'first_name': 'Test', 'last_name': 'User', 'email': 'test1@example.com', 'phone': '123', 'password': 'Pass123!'}
r = requests.post('http://127.0.0.1:8000/api/v1/auth/register', json=data)
print(f'Register: {r.status_code}')
if r.text:
    user = r.json()
    print(f'  User ID: {user.get("id")}\n')

# Login
r = requests.post('http://127.0.0.1:8000/api/v1/auth/login', json={'email': 'test1@example.com', 'password': 'Pass123!'})
print(f'Login: {r.status_code}')
if r.text:
    token = r.json().get('access_token')
    print(f'  Token: {token[:20]}...\n')
    
    # Test users endpoint
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get('http://127.0.0.1:8000/api/v1/users', headers=headers)
    print(f'GET /api/v1/users: {r.status_code}')
    print(f'  Response length: {len(r.text)}')
    if r.text:
        print(f'  Response: {r.text[:200]}\n')
    else:
        print(f'  Response: (empty)\n')
    
    # Test categories
    r = requests.post('http://127.0.0.1:8000/api/v1/categories', 
                     json={'name': 'Fiction', 'description': 'Fiction books'},
                     headers=headers)
    print(f'POST /api/v1/categories: {r.status_code}')
    if r.text:
        print(f'  Response: {r.text[:200]}\n')
    else:
        print(f'  Response: (empty)\n')
