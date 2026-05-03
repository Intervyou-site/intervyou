"""
Advanced Rate Limiting and Abuse Protection
Implements rate limiting, bot detection, and anti-scraping measures
"""
import time
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
from collections import defaultdict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import re

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Advanced rate limiter with multiple strategies:
    - Fixed window rate limiting
    - Sliding window rate limiting
    - Token bucket algorithm
    - IP-based and user-based limiting
    """
    
    def __init__(self):
        # Store: {key: [(timestamp, count), ...]}
        self.requests: Dict[str, List[Tuple[float, int]]] = defaultdict(list)
        
        # Blocked IPs: {ip: (block_until_timestamp, reason)}
        self.blocked_ips: Dict[str, Tuple[float, str]] = {}
        
        # Suspicious activity tracking
        self.suspicious_activity: Dict[str, int] = defaultdict(int)
        
        # Token buckets: {key: (tokens, last_refill_time)}
        self.token_buckets: Dict[str, Tuple[float, float]] = {}
    
    def _get_client_key(self, request: Request, user_id: Optional[int] = None) -> str:
        """Generate unique key for client (IP + user_id if available)"""
        ip = self._get_client_ip(request)
        if user_id:
            return f"user:{user_id}:{ip}"
        return f"ip:{ip}"
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        # Check proxy headers first
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def _clean_old_requests(self, key: str, window_seconds: int):
        """Remove requests older than the window"""
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        
        if key in self.requests:
            self.requests[key] = [
                (ts, count) for ts, count in self.requests[key]
                if ts > cutoff_time
            ]
    
    def check_rate_limit(
        self,
        request: Request,
        max_requests: int,
        window_seconds: int,
        user_id: Optional[int] = None,
        endpoint: str = "general"
    ) -> Tuple[bool, Optional[int]]:
        """
        Check if request should be rate limited
        
        Returns:
            (is_limited, retry_after_seconds)
        """
        client_key = f"{self._get_client_key(request, user_id)}:{endpoint}"
        
        # Check if IP is blocked
        ip = self._get_client_ip(request)
        if ip in self.blocked_ips:
            block_until, reason = self.blocked_ips[ip]
            if time.time() < block_until:
                retry_after = int(block_until - time.time())
                logger.warning(f"🚫 Blocked IP {ip} attempted access. Reason: {reason}")
                return True, retry_after
            else:
                # Block expired, remove it
                del self.blocked_ips[ip]
        
        # Clean old requests
        self._clean_old_requests(client_key, window_seconds)
        
        # Count requests in current window
        current_time = time.time()
        request_count = sum(count for ts, count in self.requests[client_key])
        
        if request_count >= max_requests:
            # Rate limit exceeded
            oldest_request = min(ts for ts, _ in self.requests[client_key]) if self.requests[client_key] else current_time
            retry_after = int(window_seconds - (current_time - oldest_request))
            
            # Track suspicious activity
            self.suspicious_activity[ip] += 1
            
            # Auto-block if too many rate limit violations
            if self.suspicious_activity[ip] >= 10:
                self.block_ip(ip, duration_seconds=3600, reason="Excessive rate limit violations")
            
            logger.warning(
                f"⚠️ Rate limit exceeded | IP: {ip} | Endpoint: {endpoint} | "
                f"Count: {request_count}/{max_requests} | Window: {window_seconds}s"
            )
            
            return True, retry_after
        
        # Add current request
        self.requests[client_key].append((current_time, 1))
        
        return False, None
    
    def check_token_bucket(
        self,
        request: Request,
        capacity: int,
        refill_rate: float,
        user_id: Optional[int] = None,
        endpoint: str = "general"
    ) -> Tuple[bool, Optional[int]]:
        """
        Token bucket rate limiting (smoother than fixed window)
        
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        
        Returns:
            (is_limited, retry_after_seconds)
        """
        client_key = f"{self._get_client_key(request, user_id)}:bucket:{endpoint}"
        current_time = time.time()
        
        # Initialize bucket if not exists
        if client_key not in self.token_buckets:
            self.token_buckets[client_key] = (capacity, current_time)
        
        tokens, last_refill = self.token_buckets[client_key]
        
        # Refill tokens based on time passed
        time_passed = current_time - last_refill
        tokens = min(capacity, tokens + (time_passed * refill_rate))
        
        if tokens >= 1:
            # Consume one token
            self.token_buckets[client_key] = (tokens - 1, current_time)
            return False, None
        else:
            # Not enough tokens
            retry_after = int((1 - tokens) / refill_rate)
            
            ip = self._get_client_ip(request)
            logger.warning(
                f"⚠️ Token bucket exhausted | IP: {ip} | Endpoint: {endpoint} | "
                f"Tokens: {tokens:.2f}/{capacity}"
            )
            
            return True, retry_after
    
    def block_ip(self, ip: str, duration_seconds: int, reason: str):
        """Block an IP address for a specified duration"""
        block_until = time.time() + duration_seconds
        self.blocked_ips[ip] = (block_until, reason)
        
        logger.warning(
            f"🚫 IP BLOCKED | IP: {ip} | Duration: {duration_seconds}s | Reason: {reason}"
        )
    
    def unblock_ip(self, ip: str):
        """Manually unblock an IP address"""
        if ip in self.blocked_ips:
            del self.blocked_ips[ip]
            logger.info(f"✅ IP unblocked: {ip}")
    
    def is_ip_blocked(self, ip: str) -> Tuple[bool, Optional[str]]:
        """Check if IP is blocked"""
        if ip in self.blocked_ips:
            block_until, reason = self.blocked_ips[ip]
            if time.time() < block_until:
                return True, reason
            else:
                del self.blocked_ips[ip]
        return False, None
    
    def reset_client(self, request: Request, user_id: Optional[int] = None):
        """Reset rate limit for a client (e.g., after successful login)"""
        client_key = self._get_client_key(request, user_id)
        
        # Remove all entries for this client
        keys_to_remove = [key for key in self.requests.keys() if key.startswith(client_key)]
        for key in keys_to_remove:
            del self.requests[key]
        
        # Reset suspicious activity
        ip = self._get_client_ip(request)
        if ip in self.suspicious_activity:
            self.suspicious_activity[ip] = 0


class BotDetector:
    """
    Detect and block bots and automated scripts
    """
    
    # Known bot user agents
    BOT_USER_AGENTS = [
        r'bot', r'crawler', r'spider', r'scraper', r'curl', r'wget',
        r'python-requests', r'scrapy', r'selenium', r'phantomjs',
        r'headless', r'automation', r'postman'
    ]
    
    # Suspicious patterns
    SUSPICIOUS_PATTERNS = {
        'rapid_requests': 10,  # More than 10 requests in 1 second
        'no_user_agent': True,
        'suspicious_user_agent': True,
        'no_referer': True,  # No referer on form submissions
        'sequential_ids': True,  # Accessing sequential resource IDs
    }
    
    def __init__(self):
        self.request_history: Dict[str, List[float]] = defaultdict(list)
        self.accessed_resources: Dict[str, List[int]] = defaultdict(list)
    
    def is_bot(self, request: Request) -> Tuple[bool, Optional[str]]:
        """
        Detect if request is from a bot
        
        Returns:
            (is_bot, reason)
        """
        user_agent = request.headers.get("user-agent", "").lower()
        
        # Check for missing user agent
        if not user_agent:
            return True, "Missing user agent"
        
        # Check for known bot user agents
        for pattern in self.BOT_USER_AGENTS:
            if re.search(pattern, user_agent, re.IGNORECASE):
                return True, f"Bot user agent detected: {pattern}"
        
        # Check for rapid requests
        ip = self._get_client_ip(request)
        current_time = time.time()
        
        # Clean old requests (keep last 10 seconds)
        self.request_history[ip] = [
            ts for ts in self.request_history[ip]
            if current_time - ts < 10
        ]
        
        # Add current request
        self.request_history[ip].append(current_time)
        
        # Check for rapid requests (more than 10 in 1 second)
        recent_requests = [
            ts for ts in self.request_history[ip]
            if current_time - ts < 1
        ]
        
        if len(recent_requests) > 10:
            return True, f"Rapid requests detected: {len(recent_requests)} requests in 1 second"
        
        return False, None
    
    def check_sequential_access(
        self,
        request: Request,
        resource_id: int,
        threshold: int = 5
    ) -> bool:
        """
        Detect sequential resource ID access (common in scraping)
        
        Returns:
            True if suspicious sequential access detected
        """
        ip = self._get_client_ip(request)
        
        # Track accessed resource IDs
        self.accessed_resources[ip].append(resource_id)
        
        # Keep only last 10 accesses
        if len(self.accessed_resources[ip]) > 10:
            self.accessed_resources[ip] = self.accessed_resources[ip][-10:]
        
        # Check if accessing sequential IDs
        if len(self.accessed_resources[ip]) >= threshold:
            ids = sorted(self.accessed_resources[ip][-threshold:])
            is_sequential = all(
                ids[i+1] - ids[i] == 1
                for i in range(len(ids)-1)
            )
            
            if is_sequential:
                logger.warning(
                    f"🤖 Sequential access detected | IP: {ip} | IDs: {ids}"
                )
                return True
        
        return False
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"


class AntiScraping:
    """
    Additional anti-scraping measures
    """
    
    @staticmethod
    def add_honeypot_fields() -> Dict[str, str]:
        """
        Generate honeypot fields for forms
        Bots will fill these, humans won't see them
        """
        return {
            "website": "",  # Hidden field
            "phone_number": "",  # Hidden field
            "company": ""  # Hidden field
        }
    
    @staticmethod
    def check_honeypot(form_data: Dict[str, str]) -> bool:
        """
        Check if honeypot fields were filled (indicates bot)
        
        Returns:
            True if bot detected
        """
        honeypot_fields = ["website", "phone_number", "company"]
        
        for field in honeypot_fields:
            if form_data.get(field):
                logger.warning(f"🍯 Honeypot triggered: {field} field was filled")
                return True
        
        return False
    
    @staticmethod
    def generate_csrf_token(session_id: str) -> str:
        """Generate CSRF token"""
        timestamp = str(int(time.time()))
        data = f"{session_id}:{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def validate_csrf_token(token: str, session_id: str, max_age: int = 3600) -> bool:
        """Validate CSRF token"""
        # In production, implement proper CSRF validation
        # This is a simplified version
        return bool(token)


# Global instances
rate_limiter = RateLimiter()
bot_detector = BotDetector()
anti_scraping = AntiScraping()


# ================================
# RATE LIMIT DECORATORS
# ================================

def rate_limit(max_requests: int, window_seconds: int, endpoint: str = "general"):
    """
    Decorator for rate limiting endpoints
    
    Usage:
        @rate_limit(max_requests=10, window_seconds=60, endpoint="login")
        async def login_endpoint(request: Request):
            ...
    """
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            # Get user_id if available
            user_id = request.session.get("user_id")
            
            # Check rate limit
            is_limited, retry_after = rate_limiter.check_rate_limit(
                request=request,
                max_requests=max_requests,
                window_seconds=window_seconds,
                user_id=user_id,
                endpoint=endpoint
            )
            
            if is_limited:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Please try again in {retry_after} seconds.",
                        "retry_after": retry_after
                    },
                    headers={"Retry-After": str(retry_after)}
                )
            
            return await func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def token_bucket_limit(capacity: int, refill_rate: float, endpoint: str = "general"):
    """
    Decorator for token bucket rate limiting
    
    Usage:
        @token_bucket_limit(capacity=10, refill_rate=1.0, endpoint="ai_generation")
        async def generate_questions(request: Request):
            ...
    """
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            user_id = request.session.get("user_id")
            
            is_limited, retry_after = rate_limiter.check_token_bucket(
                request=request,
                capacity=capacity,
                refill_rate=refill_rate,
                user_id=user_id,
                endpoint=endpoint
            )
            
            if is_limited:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "message": f"AI generation quota exhausted. Please try again in {retry_after} seconds.",
                        "retry_after": retry_after
                    },
                    headers={"Retry-After": str(retry_after)}
                )
            
            return await func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def bot_protection(func):
    """
    Decorator for bot detection
    
    Usage:
        @bot_protection
        async def sensitive_endpoint(request: Request):
            ...
    """
    async def wrapper(request: Request, *args, **kwargs):
        is_bot, reason = bot_detector.is_bot(request)
        
        if is_bot:
            ip = bot_detector._get_client_ip(request)
            logger.warning(f"🤖 Bot detected | IP: {ip} | Reason: {reason}")
            
            # Block the IP
            rate_limiter.block_ip(ip, duration_seconds=3600, reason=f"Bot detected: {reason}")
            
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Access denied",
                    "message": "Automated access detected"
                }
            )
        
        return await func(request, *args, **kwargs)
    
    return wrapper


# ================================
# RATE LIMIT CONFIGURATIONS
# ================================

class RateLimitConfig:
    """Predefined rate limit configurations for different endpoints"""
    
    # Authentication endpoints
    LOGIN = {"max_requests": 5, "window_seconds": 300, "endpoint": "login"}  # 5 per 5 minutes
    REGISTER = {"max_requests": 3, "window_seconds": 3600, "endpoint": "register"}  # 3 per hour
    PASSWORD_RESET = {"max_requests": 100, "window_seconds": 300, "endpoint": "password_reset"}  # 100 per 5 minutes (essentially unlimited for dev)
    
    # API endpoints
    API_GENERAL = {"max_requests": 100, "window_seconds": 60, "endpoint": "api"}  # 100 per minute
    API_HEAVY = {"max_requests": 20, "window_seconds": 60, "endpoint": "api_heavy"}  # 20 per minute
    
    # AI generation endpoints (token bucket)
    AI_GENERATION = {"capacity": 10, "refill_rate": 0.1, "endpoint": "ai_generation"}  # 10 tokens, refill 1 per 10 seconds
    AI_EVALUATION = {"capacity": 20, "refill_rate": 0.2, "endpoint": "ai_evaluation"}  # 20 tokens, refill 1 per 5 seconds
    
    # Data access endpoints
    DATA_READ = {"max_requests": 200, "window_seconds": 60, "endpoint": "data_read"}  # 200 per minute
    DATA_WRITE = {"max_requests": 50, "window_seconds": 60, "endpoint": "data_write"}  # 50 per minute
    
    # Admin endpoints
    ADMIN = {"max_requests": 100, "window_seconds": 60, "endpoint": "admin"}  # 100 per minute


# ================================
# HELPER FUNCTIONS
# ================================

def check_and_block_if_needed(request: Request, threshold: int = 10):
    """
    Check if client should be blocked based on suspicious activity
    """
    ip = rate_limiter._get_client_ip(request)
    
    if rate_limiter.suspicious_activity[ip] >= threshold:
        rate_limiter.block_ip(
            ip,
            duration_seconds=3600,
            reason=f"Excessive suspicious activity: {rate_limiter.suspicious_activity[ip]} violations"
        )
        return True
    
    return False


def get_rate_limit_status(request: Request, user_id: Optional[int] = None) -> Dict:
    """
    Get current rate limit status for a client
    """
    client_key = rate_limiter._get_client_key(request, user_id)
    ip = rate_limiter._get_client_ip(request)
    
    # Count requests in last minute
    current_time = time.time()
    recent_requests = sum(
        count for key, requests in rate_limiter.requests.items()
        if key.startswith(client_key)
        for ts, count in requests
        if current_time - ts < 60
    )
    
    # Check if blocked
    is_blocked, block_reason = rate_limiter.is_ip_blocked(ip)
    
    return {
        "ip": ip,
        "requests_last_minute": recent_requests,
        "is_blocked": is_blocked,
        "block_reason": block_reason,
        "suspicious_activity_count": rate_limiter.suspicious_activity.get(ip, 0)
    }
