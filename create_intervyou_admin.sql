-- Create or update intervyouadmin@gmail.com as admin
-- Run this in Railway PostgreSQL Query tab

-- First, check if user exists
SELECT id, email, role FROM "user" WHERE email = 'intervyouadmin@gmail.com';

-- If user exists, update to admin:
UPDATE "user"
SET 
    role = 'admin',
    email_verified = 1
WHERE email = 'intervyouadmin@gmail.com';

-- If user doesn't exist, you need to register first at:
-- https://intervyou-production-5a2d.up.railway.app/register
-- Then run the UPDATE query above

-- Verify the admin user:
SELECT 
    id,
    name,
    email,
    role,
    email_verified,
    created_at
FROM "user"
WHERE email = 'intervyouadmin@gmail.com';
