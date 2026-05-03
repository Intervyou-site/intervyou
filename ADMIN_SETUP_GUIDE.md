# Admin User Setup Guide

## 🔐 How to Create Admin User

There are 3 methods to create an admin user:

---

## Method 1: Using Python Script (Recommended)

### Step 1: Run the Script Locally

```bash
python create_admin.py
```

### Step 2: Follow the Prompts

```
🔐 IntervYou Admin User Creation
============================================================

Enter admin user details:

Name (default: Admin): Admin User
Email: admin@intervyou.com
Password: YourSecurePassword123!
Confirm Password: YourSecurePassword123!

Creating admin user...

✅ Admin user created successfully!
============================================================

You can now login with:
  Email: admin@intervyou.com
  Password: YourSecurePassword123!

Admin dashboard: https://intervyou-production-5a2d.up.railway.app/admin
```

### Step 3: Login

1. Go to: https://intervyou-production-5a2d.up.railway.app/login
2. Enter admin email and password
3. Access admin dashboard: https://intervyou-production-5a2d.up.railway.app/admin

---

## Method 2: Direct Database Update (Railway)

### Step 1: Access Railway Database

1. Go to Railway Dashboard
2. Click on your PostgreSQL database
3. Click **"Data"** tab
4. Click **"Query"** tab

### Step 2: Create Admin User

Run this SQL query (replace with your details):

```sql
-- First, create the user (if not exists)
INSERT INTO "user" (name, email, password, role, email_verified, created_at)
VALUES (
    'Admin User',
    'admin@intervyou.com',
    '$argon2id$v=19$m=65536,t=3,p=4$YOUR_HASHED_PASSWORD_HERE',
    'admin',
    1,
    NOW()
)
ON CONFLICT (email) DO NOTHING;

-- Or, update existing user to admin
UPDATE "user"
SET role = 'admin', email_verified = 1
WHERE email = 'nayeemabisharan@gmail.com';
```

**Note**: For the password hash, you need to hash your password first. Use Method 1 or Method 3 instead.

---

## Method 3: Using Python Console (Local)

### Step 1: Open Python Console

```bash
python
```

### Step 2: Run These Commands

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_app_cleaned import User, get_password_hash

# Load environment
load_dotenv()

# Connect to database
database_url = os.environ.get("DATABASE_URL")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Create admin user
admin = User(
    name="Admin User",
    email="admin@intervyou.com",
    password=get_password_hash("YourSecurePassword123!"),
    role="admin",
    email_verified=1
)

session.add(admin)
session.commit()

print("✅ Admin user created!")
session.close()
```

---

## Method 4: Update Existing User to Admin

If you already have a user account, you can promote it to admin:

### Using Python Script:

```bash
python create_admin.py
```

When prompted for email, enter your existing email. The script will ask if you want to update the user to admin.

### Using SQL (Railway):

```sql
UPDATE "user"
SET role = 'admin', email_verified = 1
WHERE email = 'your-email@example.com';
```

---

## 🎯 Admin Features

Once logged in as admin, you can access:

### Admin Dashboard
- URL: `/admin`
- View all users
- View system statistics
- Manage user accounts

### Admin Actions
- View user details
- Delete users
- View user attempts and scores
- Monitor system activity

---

## 🔒 Admin Login Credentials (Example)

Here's an example admin account you can create:

```
Name: Admin User
Email: admin@intervyou.com
Password: Admin@IntervYou2026!
Role: admin
```

**⚠️ IMPORTANT**: Change the password after first login!

---

## 🧪 Test Admin Access

### Step 1: Login as Admin

1. Go to: https://intervyou-production-5a2d.up.railway.app/login
2. Enter admin email and password
3. Click "Login"

### Step 2: Access Admin Dashboard

1. After login, go to: https://intervyou-production-5a2d.up.railway.app/admin
2. Should see admin dashboard with:
   - Total users count
   - Total attempts count
   - User list
   - System statistics

### Step 3: Verify Admin Role

1. Check if you can see "Admin Dashboard" link in navigation
2. Check if you can access `/admin` route
3. Check if you can see all users

---

## 🔐 Security Best Practices

### 1. Strong Password
- At least 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- Example: `Admin@IntervYou2026!Secure`

### 2. Unique Email
- Use a dedicated admin email
- Don't use personal email for admin
- Example: `admin@intervyou.com`

### 3. Change Default Password
- Change password immediately after first login
- Use password reset feature

### 4. Limit Admin Accounts
- Only create admin accounts for trusted users
- Regularly review admin users

---

## 📋 Quick Setup Checklist

- [ ] Run `python create_admin.py`
- [ ] Enter admin name, email, password
- [ ] Confirm password
- [ ] Verify "✅ Admin user created successfully!"
- [ ] Go to login page
- [ ] Login with admin credentials
- [ ] Access `/admin` dashboard
- [ ] Verify admin features work
- [ ] Change password (optional but recommended)

---

## 🐛 Troubleshooting

### "User already exists" Error

If you get this error, the email is already registered. Options:

1. **Update existing user to admin**:
   - Run `create_admin.py` again
   - Enter the existing email
   - Choose "yes" to update to admin

2. **Use different email**:
   - Run `create_admin.py` again
   - Enter a different email

### Cannot Access Admin Dashboard

**Check 1**: Verify user role in database
```sql
SELECT email, role FROM "user" WHERE email = 'your-email@example.com';
```

Should show `role = 'admin'`

**Check 2**: Clear browser cache and cookies
- Press Ctrl+Shift+Delete
- Clear cookies
- Login again

**Check 3**: Check Railway logs
```
Look for:
"Admin access required" → User is not admin
"Login required" → User is not logged in
```

### Database Connection Error

Make sure `DATABASE_URL` is set in your `.env` file or Railway environment variables.

---

## ✅ Success Indicators

When admin is set up correctly:

1. ✅ Can login with admin credentials
2. ✅ Can access `/admin` route
3. ✅ Can see all users in admin dashboard
4. ✅ Can see system statistics
5. ✅ Can perform admin actions

---

## 📞 Need Help?

If you encounter issues:

1. Check Railway logs for errors
2. Verify database connection
3. Verify user role in database
4. Try Method 1 (Python script) - it's the most reliable

---

## 🎉 You're All Set!

Once admin is created, you can:
- Manage all users
- View system statistics
- Monitor user activity
- Access admin-only features

**Admin Dashboard**: https://intervyou-production-5a2d.up.railway.app/admin
