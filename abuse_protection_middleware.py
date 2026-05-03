"""
Abuse Protection Middleware
Automatically applies rate limiting and bot detection to all endpoints
"""
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from rate_limiter import rate_limiter, bot_detector, RateLimitConfig
from typing import Callable

logger = logging.getLogger(__name__)


class AbuseProtectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware that applies rate limiting and bot detection to all requests
    """
    
    # Endpoint-specific rate limits
    # TEMPORARILY DISABLED FOR DEVELOPMENT
    RATE_LIMITS = {
        # Authentication - DISABLED
        # "/login": RateLimitConfig.LOGIN,
        # "/register": RateLimitConfig.REGISTER,
        # "/forgot_password": RateLimitConfig.PASSWORD_RESET,  # DISABLED FOR DEV
        # "/reset_password": RateLimitConfig.PASSWORD_RESET,  # DISABLED FOR DEV
        
        # AI endpoints
        "/generate_questions": {"max_requests": 10, "window_seconds": 60},
        "/generate_fresh_questions": {"max_requests": 5, "window_seconds": 60},
        "/evaluate_answer": {"max_requests": 20, "window_seconds": 60},
        "/chat": {"max_requests": 30, "window_seconds": 60},
        
        # API endpoints
        "/api/": {"max_requests": 100, "window_seconds": 60},  # Prefix match
        
        # Data modification
        "/save_question": {"max_requests": 50, "window_seconds": 60},
        "/api/bookmarks": {"max_requests": 50, "window_seconds": 60},
    }
    
    # Endpoints that should have bot protection
    # TEMPORARILY DISABLED FOR DEVELOPMENT
    BOT_PROTECTED_ENDPOINTS = [
        # "/register",
        # "/login",
        "/admin",
        "/api/bookmarks",
        "/save_question"
    ]
    
    # Endpoints exempt from rate limiting (static files, health checks)
    EXEMPT_ENDPOINTS = [
        "/static/",
        "/health",
        "/favicon.ico"
    ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process each request through abuse protection"""
        
        path = request.url.path
        
        # Skip exempt endpoints
        if any(path.startswith(exempt) for exempt in self.EXEMPT_ENDPOINTS):
            return await call_next(request)
        
        # Get client IP
        ip = self._get_client_ip(request)
        
        # Check if IP is blocked
        is_blocked, block_reason = rate_limiter.is_ip_blocked(ip)
        if is_blocked:
            logger.warning(f"🚫 Blocked IP attempted access | IP: {ip} | Path: {path} | Reason: {block_reason}")
            
            if path.startswith("/api/"):
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Access denied",
                        "message": "Your IP has been temporarily blocked due to suspicious activity",
                        "reason": block_reason
                    }
                )
            else:
                return HTMLResponse(
                    content=self._get_blocked_page(block_reason),
                    status_code=403
                )
        
        # Bot detection for sensitive endpoints
        if any(path.startswith(endpoint) for endpoint in self.BOT_PROTECTED_ENDPOINTS):
            is_bot, bot_reason = bot_detector.is_bot(request)
            
            if is_bot:
                logger.warning(f"🤖 Bot detected | IP: {ip} | Path: {path} | Reason: {bot_reason}")
                
                # Block the IP
                rate_limiter.block_ip(ip, duration_seconds=3600, reason=f"Bot: {bot_reason}")
                
                if path.startswith("/api/"):
                    return JSONResponse(
                        status_code=403,
                        content={
                            "error": "Access denied",
                            "message": "Automated access detected"
                        }
                    )
                else:
                    return HTMLResponse(
                        content=self._get_blocked_page("Automated access detected"),
                        status_code=403
                    )
        
        # Apply rate limiting
        rate_limit_config = self._get_rate_limit_config(path)
        
        if rate_limit_config:
            # Safely get user_id from session (may not be available yet in middleware chain)
            user_id = None
            try:
                if hasattr(request, 'session') and request.session:
                    user_id = request.session.get("user_id")
            except (AttributeError, AssertionError):
                # Session middleware not yet initialized or not available
                pass
            
            endpoint_name = rate_limit_config.get("endpoint", "general")
            
            is_limited, retry_after = rate_limiter.check_rate_limit(
                request=request,
                max_requests=rate_limit_config["max_requests"],
                window_seconds=rate_limit_config["window_seconds"],
                user_id=user_id,
                endpoint=endpoint_name
            )
            
            if is_limited:
                logger.warning(
                    f"⚠️ Rate limit exceeded | IP: {ip} | Path: {path} | "
                    f"Retry after: {retry_after}s"
                )
                
                if path.startswith("/api/"):
                    return JSONResponse(
                        status_code=429,
                        content={
                            "error": "Rate limit exceeded",
                            "message": f"Too many requests. Please try again in {retry_after} seconds.",
                            "retry_after": retry_after
                        },
                        headers={"Retry-After": str(retry_after)}
                    )
                else:
                    return HTMLResponse(
                        content=self._get_rate_limit_page(retry_after),
                        status_code=429,
                        headers={"Retry-After": str(retry_after)}
                    )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        if rate_limit_config:
            response.headers["X-RateLimit-Limit"] = str(rate_limit_config["max_requests"])
            response.headers["X-RateLimit-Window"] = str(rate_limit_config["window_seconds"])
        
        return response
    
    def _get_rate_limit_config(self, path: str) -> dict:
        """Get rate limit configuration for a path"""
        # Exact match
        if path in self.RATE_LIMITS:
            return self.RATE_LIMITS[path]
        
        # Prefix match
        for endpoint_prefix, config in self.RATE_LIMITS.items():
            if path.startswith(endpoint_prefix):
                return config
        
        # Default rate limit for unspecified endpoints
        return {"max_requests": 200, "window_seconds": 60, "endpoint": "default"}
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def _get_blocked_page(self, reason: str) -> str:
        """Generate HTML page for blocked users"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Access Denied</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    background: white;
                    padding: 3rem;
                    border-radius: 12px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                    max-width: 500px;
                }}
                h1 {{
                    color: #dc2626;
                    margin-bottom: 1rem;
                    font-size: 2rem;
                }}
                p {{
                    color: #666;
                    line-height: 1.6;
                    margin-bottom: 1.5rem;
                }}
                .reason {{
                    background: #fee;
                    padding: 1rem;
                    border-radius: 6px;
                    color: #dc2626;
                    font-weight: 500;
                    margin-bottom: 1.5rem;
                }}
                .icon {{
                    font-size: 4rem;
                    margin-bottom: 1rem;
                }}
                a {{
                    color: #667eea;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🚫</div>
                <h1>Access Denied</h1>
                <p>Your access has been temporarily blocked due to suspicious activity.</p>
                <div class="reason">{reason}</div>
                <p>If you believe this is an error, please contact support.</p>
                <p><a href="/">Return to Home</a></p>
            </div>
        </body>
        </html>
        """
    
    def _get_rate_limit_page(self, retry_after: int) -> str:
        """Generate HTML page for rate limited users"""
        minutes = retry_after // 60
        seconds = retry_after % 60
        
        time_str = f"{minutes} minute{'s' if minutes != 1 else ''}" if minutes > 0 else f"{seconds} second{'s' if seconds != 1 else ''}"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rate Limit Exceeded</title>
            <meta http-equiv="refresh" content="{retry_after}">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    background: white;
                    padding: 3rem;
                    border-radius: 12px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                    max-width: 500px;
                }}
                h1 {{
                    color: #f59e0b;
                    margin-bottom: 1rem;
                    font-size: 2rem;
                }}
                p {{
                    color: #666;
                    line-height: 1.6;
                    margin-bottom: 1.5rem;
                }}
                .timer {{
                    background: #fef3c7;
                    padding: 1rem;
                    border-radius: 6px;
                    color: #f59e0b;
                    font-weight: 600;
                    font-size: 1.2rem;
                    margin-bottom: 1.5rem;
                }}
                .icon {{
                    font-size: 4rem;
                    margin-bottom: 1rem;
                }}
                a {{
                    color: #667eea;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">⏱️</div>
                <h1>Too Many Requests</h1>
                <p>You've made too many requests in a short period of time.</p>
                <div class="timer">Please wait {time_str}</div>
                <p>This page will automatically refresh when you can try again.</p>
                <p><a href="/">Return to Home</a></p>
            </div>
        </body>
        </html>
        """


# ================================
# CAPTCHA VERIFICATION (Optional)
# ================================

class CaptchaVerifier:
    """
    Simple CAPTCHA verification for high-risk operations
    """
    
    @staticmethod
    def generate_simple_captcha() -> tuple:
        """
        Generate a simple math CAPTCHA
        Returns: (question, answer)
        """
        import random
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        question = f"What is {a} + {b}?"
        answer = str(a + b)
        return question, answer
    
    @staticmethod
    def verify_captcha(user_answer: str, correct_answer: str) -> bool:
        """Verify CAPTCHA answer"""
        return user_answer.strip() == correct_answer.strip()


# ================================
# IP WHITELIST/BLACKLIST
# ================================

class IPFilter:
    """
    IP whitelist and blacklist management
    """
    
    def __init__(self):
        self.whitelist = set()
        self.blacklist = set()
    
    def add_to_whitelist(self, ip: str):
        """Add IP to whitelist (bypass rate limiting)"""
        self.whitelist.add(ip)
        logger.info(f"✅ IP added to whitelist: {ip}")
    
    def add_to_blacklist(self, ip: str):
        """Add IP to blacklist (permanent block)"""
        self.blacklist.add(ip)
        logger.warning(f"🚫 IP added to blacklist: {ip}")
    
    def remove_from_whitelist(self, ip: str):
        """Remove IP from whitelist"""
        self.whitelist.discard(ip)
    
    def remove_from_blacklist(self, ip: str):
        """Remove IP from blacklist"""
        self.blacklist.discard(ip)
    
    def is_whitelisted(self, ip: str) -> bool:
        """Check if IP is whitelisted"""
        return ip in self.whitelist
    
    def is_blacklisted(self, ip: str) -> bool:
        """Check if IP is blacklisted"""
        return ip in self.blacklist


# Global IP filter instance
ip_filter = IPFilter()
