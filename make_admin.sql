-- Make nayeemabisharan@gmail.com an admin user
-- Run this in Railway PostgreSQL Query tab

UPDATE "user"
SET 
    role = 'admin',
    email_verified = 1
WHERE email = 'nayeemabisharan@gmail.com';

-- Verify the update
SELECT 
    id,
    name,
    email,
    role,
    email_verified,
    created_at
FROM "user"
WHERE email = 'nayeemabisharan@gmail.com';
