import requests

# Login first
r = requests.post('http://127.0.0.1:8000/api/v1/auth/login', json={'email': 'test1@example.com', 'password': 'Pass123!'})
if r.status_code == 200:
    token = r.json().get('access_token')
    
    # Test users endpoint - get full response
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get('http://127.0.0.1:8000/api/v1/users', headers=headers)
    
    with open('error_response.txt', 'w') as f:
        f.write(f'Status: {r.status_code}\n')
        f.write(f'Headers: {dict(r.headers)}\n')
        f.write('Response:\n')
        f.write(r.text)
    
    print('Error response saved to error_response.txt')
