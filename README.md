pip install flask requests-oauthlib

Replace CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORIZATION_BASE_URL, TOKEN_URL, SCOPE, and API_ENDPOINT with values from your OAuth provider.
Example for Google:

CLIENT_ID = "your_google_client_id"
CLIENT_SECRET = "your_google_client_secret"
REDIRECT_URI = "http://localhost:5000/callback"
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = ["openid", "email", "profile"]
API_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"
