"""
Secure File Upload Handler
Validates file types, sizes, and content to prevent malicious uploads
"""

import os
import magic
import hashlib
import uuid
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from fastapi import UploadFile
import logging
import imghdr
import mimetypes

logger = logging.getLogger(__name__)


class SecureFileUpload:
    """Secure file upload validation and handling"""
    
    # Allowed MIME types by category
    ALLOWED_MIMES = {
        'image': {
            'image/jpeg', 'image/png', 'image/gif', 'image/webp',
            'image/svg+xml', 'image/bmp'
        },
        'video': {
            'video/mp4', 'video/webm', 'video/quicktime',
            'video/x-msvideo', 'video/mpeg'
        },
        'audio': {
            'audio/mpeg', 'audio/wav', 'audio/webm',
            'audio/ogg', 'audio/mp4', 'audio/x-m4a'
        },
        'document': {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        },
        'code': {
            'text/plain', 'text/x-python', 'text/javascript',
            'text/x-java', 'text/x-c', 'text/x-c++',
            'application/x-python-code'
        }
    }
    
    # File extensions by category
    ALLOWED_EXTENSIONS = {
        'image': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'},
        'video': {'.mp4', '.webm', '.mov', '.avi', '.mpeg', '.mpg'},
        'audio': {'.mp3', '.wav', '.webm', '.ogg', '.m4a'},
        'document': {'.pdf', '.doc', '.docx', '.txt'},
        'code': {'.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.ts', '.jsx', '.tsx'}
    }
    
    # Maximum file sizes (bytes)
    MAX_SIZES = {
        'image': 10 * 1024 * 1024,      # 10MB
        'video': 100 * 1024 * 1024,     # 100MB
        'audio': 50 * 1024 * 1024,      # 50MB
        'document': 10 * 1024 * 1024,   # 10MB
        'code': 1 * 1024 * 1024,        # 1MB
    }
    
    # Dangerous file signatures (magic bytes)
    DANGEROUS_SIGNATURES = {
        b'MZ': 'Windows executable',
        b'\x7fELF': 'Linux executable',
        b'#!/bin/sh': 'Shell script',
        b'#!/bin/bash': 'Bash script',
        b'<?php': 'PHP script',
    }
    
    @staticmethod
    def validate_filename(filename: str) -> Tuple[bool, str]:
        """
        Validate filename for security issues
        
        Returns:
            (is_valid, error_message)
        """
        if not filename:
            return False, "Filename is required"
        
        # Get just the filename without path
        filename = os.path.basename(filename)
        
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False, "Filename contains invalid characters"
        
        # Check for null bytes
        if '\x00' in filename:
            return False, "Filename contains null bytes"
        
        # Check length
        if len(filename) > 255:
            return False, "Filename is too long (max 255 characters)"
        
        # Check for hidden files
        if filename.startswith('.'):
            return False, "Hidden files are not allowed"
        
        # Check for dangerous extensions
        dangerous_exts = {
            '.exe', '.dll', '.so', '.dylib', '.bat', '.cmd', '.sh',
            '.ps1', '.vbs', '.jar', '.app', '.deb', '.rpm'
        }
        ext = Path(filename).suffix.lower()
        if ext in dangerous_exts:
            return False, f"File type {ext} is not allowed"
        
        return True, ""
    
    @staticmethod
    def validate_extension(filename: str, file_type: str) -> Tuple[bool, str]:
        """
        Validate file extension matches expected type
        
        Returns:
            (is_valid, error_message)
        """
        ext = Path(filename).suffix.lower()
        
        if not ext:
            return False, "File must have an extension"
        
        allowed = SecureFileUpload.ALLOWED_EXTENSIONS.get(file_type, set())
        if ext not in allowed:
            return False, f"Extension {ext} not allowed for {file_type}. Allowed: {', '.join(allowed)}"
        
        return True, ""
    
    @staticmethod
    def validate_size(size: int, file_type: str) -> Tuple[bool, str]:
        """
        Validate file size
        
        Returns:
            (is_valid, error_message)
        """
        if size <= 0:
            return False, "File is empty"
        
        max_size = SecureFileUpload.MAX_SIZES.get(file_type, 10 * 1024 * 1024)
        if size > max_size:
            max_mb = max_size / (1024 * 1024)
            return False, f"File too large. Maximum: {max_mb}MB"
        
        return True, ""
    
    @staticmethod
    def detect_mime_type(file_content: bytes, filename: str) -> Optional[str]:
        """
        Detect MIME type from file content (not just extension)
        
        Returns:
            MIME type string or None
        """
        try:
            # Try python-magic first (most reliable)
            mime = magic.from_buffer(file_content, mime=True)
            return mime
        except Exception as e:
            logger.warning(f"python-magic failed: {e}")
            
            # Fallback to mimetypes based on extension
            mime, _ = mimetypes.guess_type(filename)
            return mime
    
    @staticmethod
    def validate_mime_type(mime_type: str, file_type: str) -> Tuple[bool, str]:
        """
        Validate MIME type matches expected file type
        
        Returns:
            (is_valid, error_message)
        """
        if not mime_type:
            return False, "Could not determine file type"
        
        allowed = SecureFileUpload.ALLOWED_MIMES.get(file_type, set())
        if mime_type not in allowed:
            return False, f"File type {mime_type} not allowed for {file_type}"
        
        return True, ""
    
    @staticmethod
    def check_dangerous_content(file_content: bytes) -> Tuple[bool, str]:
        """
        Check for dangerous file signatures
        
        Returns:
            (is_safe, warning_message)
        """
        # Check first few bytes for dangerous signatures
        for signature, description in SecureFileUpload.DANGEROUS_SIGNATURES.items():
            if file_content.startswith(signature):
                return False, f"File appears to be a {description}"
        
        # Check for embedded scripts in images
        if b'<?php' in file_content or b'<script' in file_content.lower():
            return False, "File contains embedded scripts"
        
        return True, ""
    
    @staticmethod
    def validate_image_content(file_content: bytes) -> Tuple[bool, str]:
        """
        Validate that image file is actually an image
        
        Returns:
            (is_valid, error_message)
        """
        try:
            # Use imghdr to verify image format
            import io
            img_type = imghdr.what(io.BytesIO(file_content))
            if img_type is None:
                return False, "File is not a valid image"
            return True, ""
        except Exception as e:
            return False, f"Image validation failed: {str(e)}"
    
    @staticmethod
    def generate_safe_filename(original_filename: str) -> str:
        """
        Generate a safe, unique filename
        
        Returns:
            Safe filename with UUID
        """
        # Get extension
        ext = Path(original_filename).suffix.lower()
        
        # Generate UUID-based filename
        unique_id = uuid.uuid4().hex
        safe_filename = f"{unique_id}{ext}"
        
        return safe_filename
    
    @staticmethod
    def calculate_file_hash(file_content: bytes) -> str:
        """
        Calculate SHA-256 hash of file content
        
        Returns:
            Hex digest of file hash
        """
        return hashlib.sha256(file_content).hexdigest()
    
    @staticmethod
    async def validate_upload(
        upload_file: UploadFile,
        file_type: str,
        max_size: Optional[int] = None
    ) -> Tuple[bool, Optional[bytes], Dict[str, Any]]:
        """
        Comprehensive validation of uploaded file
        
        Args:
            upload_file: FastAPI UploadFile object
            file_type: Expected file type (image, video, audio, document, code)
            max_size: Optional custom max size (overrides default)
            
        Returns:
            (is_valid, file_content, metadata_or_error)
        """
        metadata = {}
        
        # Validate filename
        is_valid_name, name_error = SecureFileUpload.validate_filename(upload_file.filename)
        if not is_valid_name:
            return False, None, {"error": name_error}
        
        # Validate extension
        is_valid_ext, ext_error = SecureFileUpload.validate_extension(upload_file.filename, file_type)
        if not is_valid_ext:
            return False, None, {"error": ext_error}
        
        # Read file content
        try:
            file_content = await upload_file.read()
        except Exception as e:
            return False, None, {"error": f"Failed to read file: {str(e)}"}
        
        # Validate size
        file_size = len(file_content)
        size_limit = max_size or SecureFileUpload.MAX_SIZES.get(file_type, 10 * 1024 * 1024)
        is_valid_size, size_error = SecureFileUpload.validate_size(file_size, file_type)
        if not is_valid_size:
            return False, None, {"error": size_error}
        
        # Check for dangerous content
        is_safe, danger_warning = SecureFileUpload.check_dangerous_content(file_content)
        if not is_safe:
            return False, None, {"error": danger_warning}
        
        # Detect and validate MIME type
        mime_type = SecureFileUpload.detect_mime_type(file_content, upload_file.filename)
        is_valid_mime, mime_error = SecureFileUpload.validate_mime_type(mime_type, file_type)
        if not is_valid_mime:
            return False, None, {"error": mime_error}
        
        # Additional validation for images
        if file_type == 'image':
            is_valid_img, img_error = SecureFileUpload.validate_image_content(file_content)
            if not is_valid_img:
                return False, None, {"error": img_error}
        
        # Generate safe filename and hash
        safe_filename = SecureFileUpload.generate_safe_filename(upload_file.filename)
        file_hash = SecureFileUpload.calculate_file_hash(file_content)
        
        # Build metadata
        metadata = {
            "original_filename": upload_file.filename,
            "safe_filename": safe_filename,
            "file_size": file_size,
            "mime_type": mime_type,
            "file_hash": file_hash,
            "extension": Path(upload_file.filename).suffix.lower()
        }
        
        return True, file_content, metadata
    
    @staticmethod
    def save_file_securely(
        file_content: bytes,
        safe_filename: str,
        upload_dir: str,
        create_subdirs: bool = True
    ) -> Tuple[bool, str]:
        """
        Save file to disk securely
        
        Args:
            file_content: File content bytes
            safe_filename: Safe filename (from generate_safe_filename)
            upload_dir: Upload directory path
            create_subdirs: Whether to create subdirectories by date
            
        Returns:
            (success, file_path_or_error)
        """
        try:
            # Create upload directory
            upload_path = Path(upload_dir)
            
            # Optionally create date-based subdirectories
            if create_subdirs:
                from datetime import datetime
                date_dir = datetime.now().strftime("%Y/%m/%d")
                upload_path = upload_path / date_dir
            
            upload_path.mkdir(parents=True, exist_ok=True)
            
            # Full file path
            file_path = upload_path / safe_filename
            
            # Ensure we're not writing outside upload directory (path traversal check)
            if not file_path.resolve().is_relative_to(upload_path.resolve()):
                return False, "Invalid file path"
            
            # Write file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Set restrictive permissions (owner read/write only)
            os.chmod(file_path, 0o600)
            
            return True, str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return False, str(e)


# Export main class
__all__ = ['SecureFileUpload']
