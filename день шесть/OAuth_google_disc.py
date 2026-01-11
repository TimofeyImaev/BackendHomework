import aiohttp
from aiohttp import web
import secrets
import json
from pathlib import Path

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8080/callback"

sessions = {}

HTML_TEMPLATE_PATH = Path(__file__).parent / 'main.html'
with open(HTML_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    HTML_TEMPLATE = f.read()

routes = web.RouteTableDef()

@routes.get('/')
async def home(request):
    return web.Response(text=HTML_TEMPLATE, content_type='text/html')

@routes.get('/login')
async def login(request):
    state = secrets.token_urlsafe(16)
    sessions[state] = {}
    
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=https://www.googleapis.com/auth/drive.readonly"
        f"&state={state}"
        "&access_type=offline"
    )
    return web.HTTPFound(auth_url)

@routes.get('/callback')
async def callback(request):
    code = request.query.get('code')
    state = request.query.get('state')
    
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, data=data) as resp:
            token_data = await resp.json()
    
    sessions[state]["access_token"] = token_data.get('access_token')
    
    return web.HTTPFound('/')

@routes.get('/files')
async def get_files(request):
    token = None
    for session in sessions.values():
        if "access_token" in session:
            token = session["access_token"]
            break
    
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {token}"}
        
        async with session.get(
            "https://www.googleapis.com/drive/v3/files?pageSize=10",
            headers=headers
        ) as resp:
            files_data = await resp.json()
            print(files_data)
    
    files = [{"name": f["name"]} for f in files_data.get("files", [])]
    return web.json_response(files)

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8080)