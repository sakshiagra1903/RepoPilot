import base64, hashlib, hmac, json, os, time
from .config import settings

def _b64(data:bytes)->str: return base64.urlsafe_b64encode(data).rstrip(b'=').decode()
def _unb64(value:str)->bytes: return base64.urlsafe_b64decode(value+'='*((4-len(value)%4)%4))
def hash_password(value:str)->str:
    salt=os.urandom(16); digest=hashlib.pbkdf2_hmac('sha256',value.encode(),salt,310000)
    return f"pbkdf2_sha256$310000${_b64(salt)}${_b64(digest)}"
def verify_password(value:str,hashed:str)->bool:
    try:
        scheme,rounds,salt,digest=hashed.split('$')
        if scheme!='pbkdf2_sha256': return False
        actual=hashlib.pbkdf2_hmac('sha256',value.encode(),_unb64(salt),int(rounds))
        return hmac.compare_digest(actual,_unb64(digest))
    except Exception: return False
def token(subject:str,kind='access',minutes=None):
    now=int(time.time()); exp=now+(minutes or settings.access_token_minutes)*60 if kind=='access' else now+settings.refresh_token_days*86400
    header=_b64(json.dumps({'alg':'HS256','typ':'JWT'},separators=(',',':')).encode())
    payload=_b64(json.dumps({'sub':subject,'type':kind,'iat':now,'exp':exp},separators=(',',':')).encode())
    signing=f'{header}.{payload}'.encode(); sig=hmac.new(settings.secret_key.encode(),signing,hashlib.sha256).digest()
    return f'{header}.{payload}.{_b64(sig)}'
def decode(value:str,kind='access'):
    try:
        head,payload,sig=value.split('.'); signing=f'{head}.{payload}'.encode()
        expected=hmac.new(settings.secret_key.encode(),signing,hashlib.sha256).digest()
        if not hmac.compare_digest(expected,_unb64(sig)): return None
        data=json.loads(_unb64(payload))
        if data.get('type')!=kind or int(data.get('exp',0))<int(time.time()): return None
        return data
    except Exception: return None
