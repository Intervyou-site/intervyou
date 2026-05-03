"""
Create admin account: intervyouadmin@gmail.com
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()

# Import models
from fastapi_app_cleaned import User, get_password_hash

def create_intervyou_admin():
    """Create intervyouadmin@gmail.com as admin"""
    
    # Admin details
    admin_email = "intervyouadmin@gmail.com"
    admin_password = "IntervYou@Admin2026!"  # Change this after first login
    admin_name = "IntervYou Admin"
    
    # Get database URL
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found")
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
        
        # Check if user already exists
        existing_user = session.query(User).filter_by(email=admin_email).first()
        
        if existing_user:
            print(f"⚠️  User {admin_email} already exists")
            print(f"📝 Updating to admin role...")
            existing_user.role = "admin"
            existing_user.email_verified = 1
            session.commit()
            print(f"✅ User updated to admin!")
        else:
            # Create new admin user
            print(f"👤 Creating new admin user: {admin_email}")
            
            admin_user = User(
                name=admin_name,
                email=admin_email,
                password=get_password_hash(admin_password),
                role="admin",
                email_verified=1,
                created_at=datetime.utcnow()
            )
            
            session.add(admin_user)
            session.commit()
            
            print(f"✅ Admin user created successfully!")
        
        print()
        print("=" * 60)
        print("🎉 ADMIN ACCOUNT READY!")
        print("=" * 60)
        print()
        print(f"📧 Email: {admin_email}")
        print(f"🔑 Password: {admin_password}")
        print(f"👤 Name: {admin_name}")
        print(f"🔐 Role: admin")
        print()
        print("🌐 Login at:")
        print("   https://intervyou-production-5a2d.up.railway.app/login")
        print()
        print("🎯 Admin Dashboard:")
        print("   https://intervyou-production-5a2d.up.railway.app/admin")
        print()
        print("⚠️  IMPORTANT: Change the password after first login!")
        print()
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        session.close()


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("🔐 Creating IntervYou Admin Account")
    print("=" * 60)
    print()
    create_intervyou_admin()
