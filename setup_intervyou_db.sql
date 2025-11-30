-- Create database and user for IntervYou
CREATE DATABASE intervyou;
CREATE USER intervyou_user WITH PASSWORD 'TboIEiUkiQi@!HYH';
GRANT ALL PRIVILEGES ON DATABASE intervyou TO intervyou_user;

-- Connect to the database
\c intervyou

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO intervyou_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO intervyou_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO intervyou_user;

-- Success message
SELECT 'Database setup complete!' as status;
