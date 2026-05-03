"""
OAuth Configuration for Social Login
Supports Google OAuth 2.0 with enhanced state management
"""

import os
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from authlib.oauth2.rfc6749 import OAuth2Token

# Load environment variables
load_dotenv()

# Initialize OAuth with explicit configuration
oauth = OAuth()

# Register Google OAuth with explicit configuration for better state management
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account',  # Always show account selection
        'token_endpoint_auth_method': 'client_secret_post'
    },
    # Ensure proper token handling
    token_endpoint='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo'
)

