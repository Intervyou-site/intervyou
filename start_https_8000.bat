@echo off
echo Starting IntervYou with HTTPS on port 8000...
python -m uvicorn fastapi_app_cleaned:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem --reload
pause
