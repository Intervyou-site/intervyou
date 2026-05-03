"""
Quick script to make nayeemabisharan@gmail.com an admin
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Import models
from fastapi_app_cleaned import User

def make_admin():
    """Make nayeemabisharan@gmail.com an admin"""
    
    # Get database URL from Railway or local
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found")
        print("⚠️  Make sure you have .env file or Railway DATABASE_URL set")
        return False
    
    # Handle Railway's postgres:// URL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print(f"📊 Connecting to database...")
    
    try:
        # Create engine and session
        if database_url.startswith("sqlite"):
            engine = create_engine(database_url, connect_args={"check_same_thread": False})
        else:
            engine = create_engine(database_url, pool_pre_ping=True)
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Find user
        user = session.query(User).filter_by(email='nayeemabisharan@gmail.com').first()
        
        if not user:
            print(f"❌ User nayeemabisharan@gmail.com not found")
            print(f"⚠️  Please register this account first")
            return False
        
        # Update to admin
        user.role = "admin"
        user.email_verified = 1
        session.commit()
        
        print(f"✅ SUCCESS!")
        print(f"✅ nayeemabisharan@gmail.com is now an ADMIN")
        print(f"")
        print(f"🔐 You can now access:")
        print(f"   Admin Dashboard: https://intervyou-production-5a2d.up.railway.app/admin")
        print(f"")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🔐 Making nayeemabisharan@gmail.com an ADMIN")
    print("=" * 60)
    print()
    make_admin()
    print()
    print("=" * 60)
