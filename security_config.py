"""
Security Configuration for Production Deployment
Implements HTTPS enforcement, secure headers, logging, and security monitoring
"""
import os
import logging
from datetime import datetime
from typing import Optional
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets

# ================================
# LOGGING CONFIGURATION
# ================================

class SecurityLogger:
    """Centralized security logging for authentication, errors, and suspicious activity"""
    
    def __init__(self):
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Configure security logger
        self.security_logger = logging.getLogger("security")
        self.security_logger.setLevel(logging.INFO)
        
        # Security log file (authentication, authorization, suspicious activity)
        security_handler = logging.FileHandler("logs/security.log")
        security_handler.setFormatter(logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        ))
        self.security_logger.addHandler(security_handler)
        
        # Configure API error logger
        self.api_logger = logging.getLogger("api_errors")
        self.api_logger.setLevel(logging.ERROR)
        
        # API error log file
        api_handler = logging.FileHandler("logs/api_errors.log")
        api_handler.setFormatter(logging.Formatter(
            '%(asctime)s - API_ERROR - %(levelname)s - %(message)s'
        ))
        self.api_logger.addHandler(api_handler)
        
        # Configure traffic logger
        self.traffic_logger = logging.getLogger("traffic")
        self.traffic_logger.setLevel(logging.INFO)
        
        # Traffic log file (unusual patterns, rate limiting)
        traffic_handler = logging.FileHandler("logs/traffic.log")
        traffic_handler.setFormatter(logging.Formatter(
            '%(asctime)s - TRAFFIC - %(levelname)s - %(message)s'
        ))
        self.traffic_logger.addHandler(traffic_handler)
        
        # Console handler for critical issues
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        self.security_logger.addHandler(console_handler)
        self.api_logger.addHandler(console_handler)
        self.traffic_logger.addHandler(console_handler)
    
    def log_login_attempt(self, email: str, success: bool, ip: str, user_agent: str):
        """Log authentication attempts"""
        status = "SUCCESS" if success else "FAILED"
        self.security_logger.info(
            f"LOGIN_{status} | Email: {email} | IP: {ip} | UserAgent: {user_agent[:100]}"
        )
    
    def log_logout(self, user_id: int, email: str, ip: str):
        """Log user logout"""
        self.security_logger.info(
            f"LOGOUT | UserID: {user_id} | Email: {email} | IP: {ip}"
        )
    
    def log_registration(self, email: str, success: bool, ip: str):
        """Log registration attempts"""
        status = "SUCCESS" if success else "FAILED"
        self.security_logger.info(
            f"REGISTRATION_{status} | Email: {email} | IP: {ip}"
        )
    
    def log_password_reset(self, email: str, ip: str):
        """Log password reset requests"""
        self.security_logger.info(
            f"PASSWORD_RESET_REQUEST | Email: {email} | IP: {ip}"
        )
    
    def log_admin_action(self, admin_email: str, action: str, target: str, ip: str):
        """Log admin actions"""
        self.security_logger.warning(
            f"ADMIN_ACTION | Admin: {admin_email} | Action: {action} | Target: {target} | IP: {ip}"
        )
    
    def log_api_error(self, endpoint: str, error: str, user_id: Optional[int], ip: str):
        """Log API errors"""
        self.api_logger.error(
            f"ENDPOINT: {endpoint} | UserID: {user_id} | IP: {ip} | Error: {error}"
        )
    
    def log_suspicious_activity(self, activity_type: str, details: str, ip: str, user_id: Optional[int] = None):
        """Log suspicious activity"""
        self.security_logger.warning(
            f"SUSPICIOUS_{activity_type} | UserID: {user_id} | IP: {ip} | Details: {details}"
        )
    
    def log_rate_limit_exceeded(self, ip: str, endpoint: str, user_id: Optional[int] = None):
        """Log rate limit violations"""
        self.traffic_logger.warning(
            f"RATE_LIMIT_EXCEEDED | IP: {ip} | Endpoint: {endpoint} | UserID: {user_id}"
        )
    
    def log_unusual_traffic(self, pattern: str, details: str, ip: str):
        """Log unusual traffic patterns"""
        self.traffic_logger.warning(
            f"UNUSUAL_TRAFFIC | Pattern: {pattern} | IP: {ip} | Details: {details}"
        )
    
    def log_unauthorized_access(self, endpoint: str, ip: str, user_id: Optional[int] = None):
        """Log unauthorized access attempts"""
        self.security_logger.warning(
            f"UNAUTHORIZED_ACCESS | Endpoint: {endpoint} | UserID: {user_id} | IP: {ip}"
        )
    
    def log_data_access(self, user_id: int, resource_type: str, resource_id: int, action: str, ip: str):
        """Log sensitive data access"""
        self.security_logger.info(
            f"DATA_ACCESS | UserID: {user_id} | Resource: {resource_type}:{resource_id} | Action: {action} | IP: {ip}"
        )


# Global security logger instance
security_logger = SecurityLogger()


# ================================
# HTTPS ENFORCEMENT MIDDLEWARE
# ================================

class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """Enforce HTTPS in production"""
    
    async def dispatch(self, request: Request, call_next):
        # Only enforce HTTPS in production
        if os.getenv("ENVIRONMENT") == "production":
            # Check if request is not HTTPS
            if request.url.scheme != "https":
                # Check for proxy headers (common in cloud deployments)
                forwarded_proto = request.headers.get("x-forwarded-proto")
                if forwarded_proto != "https":
                    # Redirect to HTTPS
                    url = request.url.replace(scheme="https")
                    return Response(
                        status_code=301,
                        headers={"Location": str(url)}
                    )
        
        response = await call_next(request)
        return response


# ================================
# SECURITY HEADERS MIDDLEWARE
# ================================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Strict Transport Security (HSTS)
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: https:",
            "connect-src 'self' https://api.openai.com",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
        
        # X-Frame-Options (prevent clickjacking)
        response.headers["X-Frame-Options"] = "DENY"
        
        # X-Content-Type-Options (prevent MIME sniffing)
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # X-XSS-Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy - Allow camera and microphone for same origin
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(self), camera=(self)"
        
        return response


# ================================
# REQUEST LOGGING MIDDLEWARE
# ================================

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests for security monitoring"""
    
    def __init__(self, app):
        super().__init__(app)
        self.request_counts = {}  # Track requests per IP
        self.suspicious_patterns = {
            "sql_injection": [
                "' OR '",  # More specific pattern
                "1=1",
                " OR 1=1",
                "DROP TABLE",
                "DROP DATABASE",
                "SELECT * FROM",
                "UNION SELECT",
                "'; DROP",
                "--",
                "/*",
                "xp_"
            ],
            "path_traversal": ["../", "..\\", "%2e%2e"],
            "xss": ["<script", "javascript:", "onerror=", "onload="],
        }
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        # Get request details
        method = request.method
        path = request.url.path
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Track request count per IP
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {"count": 0, "last_reset": datetime.now()}
        
        # Reset counter every minute
        if (datetime.now() - self.request_counts[client_ip]["last_reset"]).seconds > 60:
            self.request_counts[client_ip] = {"count": 0, "last_reset": datetime.now()}
        
        self.request_counts[client_ip]["count"] += 1
        
        # Check for rate limiting (more than 100 requests per minute)
        if self.request_counts[client_ip]["count"] > 100:
            security_logger.log_rate_limit_exceeded(client_ip, path)
            security_logger.log_unusual_traffic(
                "HIGH_REQUEST_RATE",
                f"IP {client_ip} made {self.request_counts[client_ip]['count']} requests in 1 minute",
                client_ip
            )
        
        # Check for suspicious patterns in URL
        for pattern_type, patterns in self.suspicious_patterns.items():
            for pattern in patterns:
                if pattern.lower() in path.lower():
                    security_logger.log_suspicious_activity(
                        pattern_type.upper(),
                        f"Suspicious pattern '{pattern}' detected in URL: {path}",
                        client_ip
                    )
        
        # Log request
        start_time = datetime.now()
        
        try:
            response = await call_next(request)
            
            # Calculate response time
            duration = (datetime.now() - start_time).total_seconds()
            
            # Log slow requests (> 5 seconds)
            if duration > 5:
                security_logger.log_unusual_traffic(
                    "SLOW_REQUEST",
                    f"{method} {path} took {duration:.2f}s",
                    client_ip
                )
            
            # Log failed requests
            if response.status_code >= 400:
                if response.status_code == 401:
                    security_logger.log_unauthorized_access(path, client_ip)
                elif response.status_code >= 500:
                    security_logger.log_api_error(
                        path,
                        f"Server error: {response.status_code}",
                        None,
                        client_ip
                    )
            
            return response
            
        except Exception as e:
            # Log unhandled exceptions
            security_logger.log_api_error(path, str(e), None, client_ip)
            raise


# ================================
# SECRETS MANAGEMENT
# ================================

class SecretsManager:
    """Secure secrets management"""
    
    @staticmethod
    def validate_environment():
        """Validate that all required secrets are set in production"""
        if os.getenv("ENVIRONMENT") == "production":
            required_secrets = [
                "SECRET_KEY",
                "DATABASE_URL",
                "OPENAI_API_KEY"
            ]
            
            missing_secrets = []
            for secret in required_secrets:
                value = os.getenv(secret)
                if not value or value.startswith("your-") or value == "change-me":
                    missing_secrets.append(secret)
            
            if missing_secrets:
                raise ValueError(
                    f"Missing or invalid production secrets: {', '.join(missing_secrets)}"
                )
            
            # Validate SECRET_KEY strength
            secret_key = os.getenv("SECRET_KEY")
            if len(secret_key) < 32:
                raise ValueError("SECRET_KEY must be at least 32 characters long")
            
            # Validate DATABASE_URL is not SQLite in production
            db_url = os.getenv("DATABASE_URL", "")
            if "sqlite" in db_url.lower():
                raise ValueError("SQLite is not recommended for production. Use PostgreSQL.")
    
    @staticmethod
    def generate_secret_key() -> str:
        """Generate a secure secret key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def mask_secret(secret: str, visible_chars: int = 4) -> str:
        """Mask a secret for logging"""
        if not secret or len(secret) <= visible_chars:
            return "****"
        return secret[:visible_chars] + "*" * (len(secret) - visible_chars)


# ================================
# DATABASE SECURITY
# ================================

class DatabaseSecurity:
    """Database security configuration"""
    
    @staticmethod
    def get_secure_database_url() -> str:
        """Get database URL with security checks"""
        db_url = os.getenv("DATABASE_URL")
        
        if not db_url:
            raise ValueError("DATABASE_URL not set")
        
        # In production, ensure SSL is enabled for PostgreSQL
        if os.getenv("ENVIRONMENT") == "production" and "postgresql" in db_url:
            if "sslmode" not in db_url:
                # Add SSL mode if not present
                separator = "&" if "?" in db_url else "?"
                db_url = f"{db_url}{separator}sslmode=require"
        
        return db_url
    
    @staticmethod
    def validate_database_connection():
        """Validate database connection security"""
        db_url = os.getenv("DATABASE_URL", "")
        
        if os.getenv("ENVIRONMENT") == "production":
            # Check for localhost/127.0.0.1 in production
            if "localhost" in db_url or "127.0.0.1" in db_url:
                security_logger.security_logger.warning(
                    "DATABASE_WARNING | Database URL contains localhost in production"
                )
            
            # Check for default passwords
            if "password" in db_url.lower() or "123456" in db_url:
                security_logger.security_logger.error(
                    "DATABASE_SECURITY | Weak or default password detected in DATABASE_URL"
                )


# ================================
# CONFIGURATION HELPER
# ================================

def configure_security(app):
    """Configure all security middleware and settings"""
    
    # Validate environment
    SecretsManager.validate_environment()
    DatabaseSecurity.validate_database_connection()
    
    # Add HTTPS redirect middleware (first, so it runs before others)
    app.add_middleware(HTTPSRedirectMiddleware)
    
    # Add security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Configure CORS
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    if allowed_origins and allowed_origins[0]:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            allow_headers=["*"],
        )
    
    # Add trusted host middleware (prevent host header attacks)
    if os.getenv("ENVIRONMENT") == "production":
        trusted_hosts = os.getenv("TRUSTED_HOSTS", "").split(",")
        if trusted_hosts and trusted_hosts[0]:
            app.add_middleware(
                TrustedHostMiddleware,
                allowed_hosts=trusted_hosts
            )
    
    # Configure session middleware with secure settings
    secret_key = os.getenv("SECRET_KEY")
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
        session_cookie="session",
        max_age=86400,  # 24 hours
        same_site="lax",
        https_only=os.getenv("ENVIRONMENT") == "production"
    )
    
    # Log security configuration
    security_logger.security_logger.info(
        f"Security configuration completed | Environment: {os.getenv('ENVIRONMENT')} | "
        f"HTTPS: {os.getenv('ENVIRONMENT') == 'production'}"
    )
    
    return app


# ================================
# HELPER FUNCTIONS
# ================================

def get_client_ip(request: Request) -> str:
    """Get client IP address from request"""
    # Check for proxy headers first
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    # Check for other proxy headers
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    
    # Fall back to direct client IP
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """Get user agent from request"""
    return request.headers.get("user-agent", "unknown")
