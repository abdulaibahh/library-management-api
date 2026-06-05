import requests

# Login first
r = requests.post('http://127.0.0.1:8000/api/v1/auth/login', json={'email': 'test1@example.com', 'password': 'Pass123!'})
if r.status_code == 200:
    token = r.json().get('access_token')
    print(f'Token obtained: {token[:30]}...\n')
    
    # Test users endpoint - get full response
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get('http://127.0.0.1:8000/api/v1/users', headers=headers)
    print(f'GET /api/v1/users: {r.status_code}')
    print('Full response:')
    print(r.text[:2000])
else:
    print('Login failed')
