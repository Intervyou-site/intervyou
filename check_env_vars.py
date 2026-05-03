"""
Environment Variables Diagnostic Script
Run this to check if Railway environment variables are loaded
"""

import os
import sys

def check_env_vars():
    """Check if all required environment variables are set"""
    
    print("=" * 70)
    print("🔍 ENVIRONMENT VARIABLES DIAGNOSTIC")
    print("=" * 70)
    print()
    
    # Check environment
    env = os.environ.get("ENVIRONMENT", "not set")
    print(f"ENVIRONMENT: {env}")
    print()
    
    # Required email variables
    email_vars = {
        "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
        "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD"),
        "SMTP_HOST": os.environ.get("SMTP_HOST"),
        "SMTP_PORT": os.environ.get("SMTP_PORT"),
        "MAIL_FROM": os.environ.get("MAIL_FROM"),
        "MAIL_FROM_NAME": os.environ.get("MAIL_FROM_NAME"),
    }
    
    print("📧 EMAIL CONFIGURATION:")
    print("-" * 70)
    
    all_set = True
    for var_name, var_value in email_vars.items():
        if var_value:
            if "PASSWORD" in var_name:
                # Mask password
                masked = "*" * len(var_value) if len(var_value) > 0 else "EMPTY"
                print(f"✅ {var_name:20} = {masked} (length: {len(var_value)})")
            else:
                print(f"✅ {var_name:20} = {var_value}")
        else:
            print(f"❌ {var_name:20} = NOT SET")
            all_set = False
    
    print()
    print("-" * 70)
    
    if all_set:
        print("✅ All email variables are set!")
        print()
        print("🧪 Testing email service import...")
        try:
            from email_service import email_service
            print(f"✅ Email service imported successfully")
            print(f"✅ Email service configured: {email_service.is_configured}")
            
            if email_service.is_configured:
                print()
                print("🎉 EMAIL SERVICE IS READY!")
                print()
                print("You can now test sending emails.")
                return True
            else:
                print()
                print("❌ Email service not configured despite variables being set")
                print("⚠️  Check email_service.py initialization")
                return False
                
        except Exception as e:
            print(f"❌ Failed to import email service: {e}")
            return False
    else:
        print("❌ Some email variables are missing!")
        print()
        print("📋 TO FIX:")
        print("1. Go to Railway Dashboard")
        print("2. Click on your service")
        print("3. Click 'Variables' tab")
        print("4. Add missing variables")
        print("5. Redeploy")
        return False
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    success = check_env_vars()
    sys.exit(0 if success else 1)
