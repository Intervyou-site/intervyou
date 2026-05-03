"""
Admin User Creation Script
Run this script to create an admin user in the database
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Load environment variables
load_dotenv()

# Import models
from fastapi_app_cleaned import User, Base, get_password_hash

def create_admin_user(email: str, password: str, name: str = "Admin"):
    """Create an admin user in the database"""
    
    # Get database URL
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
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
        existing_user = session.query(User).filter_by(email=email).first()
        
        if existing_user:
            print(f"⚠️  User with email {email} already exists")
            response = input("Do you want to update this user to admin? (yes/no): ")
            
            if response.lower() in ['yes', 'y']:
                existing_user.role = "admin"
                existing_user.email_verified = 1
                session.commit()
                print(f"✅ User {email} updated to admin role")
                return True
            else:
                print("❌ Operation cancelled")
                return False
        
        # Create new admin user
        print(f"👤 Creating admin user: {email}")
        
        admin_user = User(
            name=name,
            email=email,
            password=get_password_hash(password),
            role="admin",
            email_verified=1,
            created_at=datetime.utcnow()
        )
        
        session.add(admin_user)
        session.commit()
        
        print(f"✅ Admin user created successfully!")
        print(f"📧 Email: {email}")
        print(f"👤 Name: {name}")
        print(f"🔑 Role: admin")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False
    finally:
        session.close()


def main():
    """Main function"""
    print("=" * 60)
    print("🔐 IntervYou Admin User Creation")
    print("=" * 60)
    print()
    
    # Get admin details
    print("Enter admin user details:")
    print()
    
    name = input("Name (default: Admin): ").strip() or "Admin"
    email = input("Email: ").strip()
    
    if not email:
        print("❌ Email is required")
        return
    
    password = input("Password: ").strip()
    
    if not password:
        print("❌ Password is required")
        return
    
    if len(password) < 8:
        print("❌ Password must be at least 8 characters")
        return
    
    confirm_password = input("Confirm Password: ").strip()
    
    if password != confirm_password:
        print("❌ Passwords do not match")
        return
    
    print()
    print("Creating admin user...")
    print()
    
    success = create_admin_user(email, password, name)
    
    if success:
        print()
        print("=" * 60)
        print("✅ Admin user created successfully!")
        print("=" * 60)
        print()
        print("You can now login with:")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print()
        print("Admin dashboard: https://intervyou-production-5a2d.up.railway.app/admin")
        print()
    else:
        print()
        print("❌ Failed to create admin user")
        print()


if __name__ == "__main__":
    main()
