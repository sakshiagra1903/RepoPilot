from app.analyzer import analyze, retrieve
from app.security import hash_password, verify_password, token, decode

def test_password_hash_and_tokens():
 h=hash_password("correct horse battery staple")
 assert h != "correct horse battery staple" and verify_password("correct horse battery staple",h)
 assert decode(token("7"))["sub"]=="7"
 assert decode(token("7","refresh")) is None

def test_analyzer_heuristics_and_counts():
 result=analyze([{"path":"src/app.py","content":"password = 'supersecret123'\nimport pickle\npickle.loads(data)\n"}])
 assert result["file_count"]==1 and len(result["findings"])>=2
 assert all(x["verification_status"]=="unverified heuristic" for x in result["findings"])

def test_retrieval_returns_exact_source_lines():
 files=[{"path":"auth.py","content":"def login(user):\n    return verify(user)\n"}]
 hits=retrieve(files,"where is login implemented")
 assert hits and hits[0]["path"]=="auth.py" and hits[0]["start_line"]==1

def test_auth_api_register_and_protected_profile():
    from fastapi.testclient import TestClient
    from app.main import app
    import uuid
    client=TestClient(app)
    email=f"test-{uuid.uuid4().hex[:10]}@example.com"
    response=client.post('/api/v1/auth/register',json={"email":email,"password":"a-strong-test-password","full_name":"Test Developer"})
    assert response.status_code==201
    access=response.json()['access_token']
    profile=client.get('/api/v1/auth/me',headers={"Authorization":f"Bearer {access}"})
    assert profile.status_code==200 and profile.json()['email']==email
    assert client.get('/api/v1/auth/me').status_code==401
