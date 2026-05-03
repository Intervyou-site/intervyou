"""
OAuth Configuration for Social Login
Supports Google OAuth 2.0
"""

import os
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth

# Load environment variables
load_dotenv()

# Initialize OAuth
oauth = OAuth()

# Register Google OAuth with explicit configuration
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account'  # Always show account selection
    }
)
