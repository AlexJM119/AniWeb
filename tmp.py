import requests
import json
import secrets

MAL_ID = '88bda1ac42a3e73fbed3bf6c578d068c'
MAL_SECRET = '88b595548c67d1055f72f3c945c8d6370d61a8cb6507856c711043478f73d683'
MAL_BASE = 'https://api.myanimelist.net/v2'

def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

code_verifier = code_challenge = get_new_code_verifier()
auth_r = requests.get('https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id='+MAL_ID+'&state=RequestID01&client_challenge='+code_challenge)
