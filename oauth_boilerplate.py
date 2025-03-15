from flask import Flask, request, redirect, session, url_for, render_template_string
from requests_oauthlib import OAuth2Session
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key for session management

# OAuth 2.0 configuration (replace with your provider's details)
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
REDIRECT_URI = "http://localhost:5000/callback"
AUTHORIZATION_BASE_URL = "https://provider.com/oauth2/authorize"  # e.g., "https://accounts.google.com/o/oauth2/v2/auth" for Google
TOKEN_URL = "https://provider.com/oauth2/token"  # e.g., "https://oauth2.googleapis.com/token" for Google
SCOPE = ["read", "write"]  # Adjust scopes: e.g., ["openid", "email", "profile"] for Google
API_ENDPOINT = "https://provider.com/api/user"  # e.g., "https://api.github.com/user" for GitHub

# Helper function to create OAuth2Session
def get_oauth_client(token=None):
    return OAuth2Session(
        CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        token=token
    )

# Home page
@app.route("/")
def home():
    if "oauth_token" in session:
        return redirect(url_for("profile"))
    return render_template_string("""
        <h1>Welcome</h1>
        <a href="{{ url_for('login') }}">Login with OAuth</a>
    """)

# Start the OAuth flow
@app.route("/login")
def login():
    oauth = get_oauth_client()
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
    session["oauth_state"] = state  # Store state for CSRF protection
    return redirect(authorization_url)

# Callback route after authorization
@app.route("/callback")
def callback():
    oauth = get_oauth_client()
    try:
        token = oauth.fetch_token(
            TOKEN_URL,
            client_secret=CLIENT_SECRET,
            authorization_response=request.url,
            state=session.get("oauth_state")
        )
        session["oauth_token"] = token
        return redirect(url_for("profile"))
    except Exception as e:
        return render_template_string(f"<h1>Error</h1><p>{str(e)}</p>")

# Profile page (protected route)
@app.route("/profile")
def profile():
    token = session.get("oauth_token")
    if not token:
        return redirect(url_for("login"))

    oauth = get_oauth_client(token)
    try:
        response = oauth.get(API_ENDPOINT)
        user_data = response.json()
        return render_template_string("""
            <h1>Profile</h1>
            <pre>{{ user_data }}</pre>
            <a href="{{ url_for('logout') }}">Logout</a>
        """, user_data=user_data)
    except Exception as e:
        return render_template_string(f"<h1>Error</h1><p>{str(e)}</p>")

# Logout route
@app.route("/logout")
def logout():
    session.pop("oauth_token", None)
    session.pop("oauth_state", None)
    return redirect(url_for("home"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)