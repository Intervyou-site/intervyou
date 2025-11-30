# oauth_config.py
"""
OAuth Configuration for Social Login
Supports Google OAuth 2.0
"""

import os
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

# Load environment variables
config = Config('.env')

# Initialize OAuth
oauth = OAuth(config)

# Google OAuth
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
