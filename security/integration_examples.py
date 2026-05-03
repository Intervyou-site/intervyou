"""
Integration Examples
Shows how to apply security validators to existing endpoints
"""

from fastapi import FastAPI, Depends, Request, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional

# Import security modules
from security import (
    InputValidator,
    SecureQueryBuilder,
    SecureDBOperations,
    SecureFileUpload,
    CodeSecurityValidator,
    QuestionSubmissionRequest,
    CodeExecutionRequest,
    SearchRequest,
    PaginationRequest,
    FilterRequest,
)


# ============================================================================
# EXAMPLE 1: Secure Question Submission with Validation
# ============================================================================

async def secure_evaluate_answer(
    request: QuestionSubmissionRequest,
    http_request: Request,
    db: Session
):
    """
    Secure version of /evaluate_answer endpoint
    """
    # Get current user
    user = get_current_user(http_request, db)
    if not user:
        return {"error": "Not authenticated"}, 401
    
    # Input is already validated by Pydantic model
    # Additional SQL injection check
    is_safe_q, _ = InputValidator.check_sql_injection(request.question)
    is_safe_a, _ = InputValidator.check_sql_injection(request.answer)
    
    if not is_safe_q or not is_safe_a:
        return {"error": "Invalid input detected"}, 400
    
    # Process with validated data
    evaluation = await evaluate_answer_service(
        question=request.question,
        answer=request.answer,
        category=request.category,
        difficulty=request.difficulty
    )
    
    # Save to database securely
    attempt_data = {
        'user_id': user.id,
        'question': request.question,
        'score': evaluation['overall_score'],
        'feedback': json.dumps(evaluation)
    }
    
    attempt = SecureDBOperations.safe_create(
        db=db,
        model=Attempt,
        data=attempt_data,
        allowed_fields=['user_id', 'question', 'score', 'feedback', 'timestamp']
    )
    
    if attempt:
        db.commit()
    
    return {"evaluation": evaluation}


# ============================================================================
# EXAMPLE 2: Secure Bookmark Retrieval with Filtering
# ============================================================================

async def secure_get_bookmarks(
    http_request: Request,
    db: Session,
    filters: FilterRequest = Depends(),
    pagination: PaginationRequest = Depends()
):
    """
    Secure version of /api/bookmarks endpoint
    """
    user = get_current_user(http_request, db)
    if not user:
        return {"error": "Not authenticated"}, 401
    
    # Start with base query
    query = db.query(SavedQuestion).filter(SavedQuestion.user_id == user.id)
    
    # Build secure filters
    filter_dict = {}
    if filters.category:
        filter_dict['category'] = filters.category
    if filters.company:
        # Sanitize company name
        safe_company = InputValidator.sanitize_string(filters.company, max_length=100)
        filter_dict['company'] = safe_company
    if filters.difficulty:
        filter_dict['difficulty'] = filters.difficulty
    
    # Apply filters securely
    if filter_dict:
        conditions = SecureQueryBuilder.build_filter(
            model=SavedQuestion,
            filters=filter_dict,
            allowed_columns=['category', 'company', 'difficulty', 'priority']
        )
        if conditions:
            from sqlalchemy import and_
            query = query.filter(and_(*conditions))
    
    # Apply search if provided
    if filters.search:
        # Validate search query
        is_valid, safe_search, error = QueryParameterValidator.validate_search_query(
            filters.search,
            min_length=1,
            max_length=200
        )
        if is_valid:
            query = SecureQueryBuilder.safe_search(
                query=query,
                model=SavedQuestion,
                search_term=safe_search,
                search_columns=['question', 'notes', 'company']
            )
    
    # Apply sorting
    query = SecureQueryBuilder.apply_sorting(
        query=query,
        model=SavedQuestion,
        sort_by=pagination.sort_by,
        order=pagination.order,
        allowed_columns=['timestamp', 'priority', 'category', 'difficulty']
    )
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    query = SecureQueryBuilder.apply_pagination(
        query=query,
        page=pagination.page,
        limit=pagination.limit,
        max_limit=100
    )
    
    # Execute query
    results = query.all()
    
    return {
        "success": True,
        "bookmarks": [bookmark_to_dict(b) for b in results],
        "total": total,
        "page": pagination.page,
        "limit": pagination.limit
    }


# ============================================================================
# EXAMPLE 3: Secure Code Execution
# ============================================================================

async def secure_execute_code(
    request: CodeExecutionRequest,
    http_request: Request,
    db: Session
):
    """
    Secure version of /ide/execute endpoint
    """
    user = get_current_user(http_request, db)
    if not user:
        return {"error": "Not authenticated"}, 401
    
    # Validate code execution request
    is_valid, result = CodeSecurityValidator.validate_execution_request(
        code=request.code,
        language=request.language,
        input_data=request.input_data,
        strict_mode=True  # Reject dangerous patterns
    )
    
    if not is_valid:
        return {
            "success": False,
            "error": result.get('error', 'Code validation failed'),
            "violations": result.get('violations', [])
        }
    
    # Execute code with sanitized input
    from online_ide.code_executor import CodeExecutor
    executor = CodeExecutor()
    
    execution_result = executor.execute_code(
        code=request.code,
        language=request.language,
        input_data=result['sanitized_input']
    )
    
    # Add warnings if any
    if result.get('warnings'):
        execution_result['security_warnings'] = result['warnings']
    
    return execution_result


# ============================================================================
# EXAMPLE 4: Secure File Upload
# ============================================================================

async def secure_upload_video(
    http_request: Request,
    video: UploadFile = File(...),
    question: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Secure version of /upload_video endpoint
    """
    user = get_current_user(http_request, db)
    if not user:
        return {"error": "Not authenticated"}
    
    # Validate question if provided
    if question:
        question = InputValidator.sanitize_string(question, max_length=2000)
        is_safe, _ = InputValidator.check_sql_injection(question)
        if not is_safe:
            return {"error": "Invalid question format"}
    
    # Validate video upload
    is_valid, file_content, result = await SecureFileUpload.validate_upload(
        upload_file=video,
        file_type='video',
        max_size=100 * 1024 * 1024  # 100MB
    )
    
    if not is_valid:
        return {
            "success": False,
            "error": result.get('error', 'File validation failed')
        }
    
    # Check file size (must be at least 10KB)
    if result['file_size'] < 10000:
        return {
            "success": False,
            "error": "Video is too short or empty"
        }
    
    # Save file securely
    success, file_path = SecureFileUpload.save_file_securely(
        file_content=file_content,
        safe_filename=result['safe_filename'],
        upload_dir='uploads/videos',
        create_subdirs=True
    )
    
    if not success:
        return {
            "success": False,
            "error": "Failed to save video file"
        }
    
    # Process video
    try:
        analysis = await analyze_video_response(
            video_path=file_path,
            question=question,
            user_id=user.id
        )
        
        # Clean up temp file
        import os
        try:
            os.unlink(file_path)
        except:
            pass
        
        return {
            "success": True,
            "analysis": analysis,
            "file_hash": result['file_hash']
        }
    except Exception as e:
        logger.error(f"Video analysis error: {e}")
        return {
            "success": False,
            "error": "Video analysis failed"
        }


# ============================================================================
# EXAMPLE 5: Secure Search with SQL Injection Prevention
# ============================================================================

async def secure_search_questions(
    request: SearchRequest,
    http_request: Request,
    db: Session
):
    """
    Secure version of /api/questions/search endpoint
    """
    user = get_current_user(http_request, db)
    if not user:
        return {"error": "Not authenticated"}, 401
    
    # Query is already validated by Pydantic
    # Additional validation
    is_valid, safe_query, error = QueryParameterValidator.validate_search_query(
        request.query,
        min_length=1,
        max_length=200
    )
    
    if not is_valid:
        return {"error": error}, 400
    
    # Build secure search query
    query = db.query(SavedQuestion).filter(SavedQuestion.user_id == user.id)
    
    # Apply category filter if provided
    if request.category:
        query = query.filter(SavedQuestion.category == request.category)
    
    # Apply safe search
    query = SecureQueryBuilder.safe_search(
        query=query,
        model=SavedQuestion,
        search_term=safe_query,
        search_columns=['question', 'notes', 'company']
    )
    
    # Apply limit
    query = query.limit(request.limit)
    
    results = query.all()
    
    return {
        "success": True,
        "query": safe_query,
        "count": len(results),
        "results": [question_to_dict(q) for q in results]
    }


# ============================================================================
# EXAMPLE 6: Secure Database Update with Field Validation
# ============================================================================

async def secure_update_bookmark(
    question_id: int,
    http_request: Request,
    db: Session
):
    """
    Secure version of /api/bookmarks/{question_id} PUT endpoint
    """
    user = get_current_user(http_request, db)
    if not user:
        return {"error": "Not authenticated"}, 401
    
    # Get update data from request
    data = await http_request.json()
    
    # Validate and sanitize update data
    update_data = {}
    
    if 'notes' in data:
        update_data['notes'] = InputValidator.sanitize_string(
            data['notes'],
            max_length=2000
        )
    
    if 'priority' in data:
        is_valid, priority, error = InputValidator.validate_integer(
            data['priority'],
            min_val=0,
            max_val=5
        )
        if is_valid:
            update_data['priority'] = priority
    
    if 'tags' in data:
        if isinstance(data['tags'], list):
            # Validate each tag
            validated_tags = []
            for tag in data['tags'][:10]:  # Max 10 tags
                tag = InputValidator.sanitize_string(tag, max_length=50)
                if tag:
                    validated_tags.append(tag)
            update_data['tags'] = validated_tags
    
    # Update record securely
    updated = SecureDBOperations.safe_update(
        db=db,
        model=SavedQuestion,
        record_id=question_id,
        data=update_data,
        allowed_fields=['notes', 'priority', 'tags', 'difficulty'],
        user_id=user.id  # Ensure user owns the record
    )
    
    if not updated:
        return {"error": "Question not found or access denied"}, 404
    
    db.commit()
    
    return {
        "success": True,
        "question": question_to_dict(updated)
    }


# ============================================================================
# EXAMPLE 7: Secure Admin Operation with Authorization
# ============================================================================

async def secure_admin_delete_user(
    user_id: int,
    http_request: Request,
    db: Session
):
    """
    Secure version of /admin/user/{user_id} DELETE endpoint
    """
    # Get admin user
    admin = get_current_user(http_request, db)
    if not admin or admin.role != 'admin':
        return {"error": "Unauthorized"}, 403
    
    # Validate user_id
    is_valid, validated_id, error = InputValidator.validate_integer(
        user_id,
        min_val=1,
        max_val=999999999
    )
    
    if not is_valid:
        return {"error": error}, 400
    
    # Prevent admin from deleting themselves
    if validated_id == admin.id:
        return {"error": "Cannot delete your own account"}, 400
    
    # Get user to delete
    user_to_delete = SecureDBOperations.safe_get_by_id(
        db=db,
        model=User,
        record_id=validated_id
    )
    
    if not user_to_delete:
        return {"error": "User not found"}, 404
    
    # Prevent deleting other admins
    if user_to_delete.role == 'admin':
        return {"error": "Cannot delete other admin accounts"}, 403
    
    # Delete user
    success = SecureDBOperations.safe_delete(
        db=db,
        model=User,
        record_id=validated_id
    )
    
    if success:
        db.commit()
        logger.info(f"Admin {admin.email} deleted user {user_to_delete.email}")
        return {"success": True, "message": "User deleted"}
    else:
        return {"error": "Failed to delete user"}, 500


# ============================================================================
# Helper Functions
# ============================================================================

def bookmark_to_dict(bookmark):
    """Convert bookmark to dictionary"""
    return {
        "id": bookmark.id,
        "question": bookmark.question,
        "category": bookmark.category,
        "company": bookmark.company,
        "notes": bookmark.notes,
        "tags": bookmark.tags,
        "priority": bookmark.priority,
        "timestamp": bookmark.timestamp.isoformat() if bookmark.timestamp else None
    }


def question_to_dict(question):
    """Convert question to dictionary"""
    return {
        "id": question.id,
        "question": question.question,
        "category": question.category,
        "difficulty": question.difficulty
    }


# ============================================================================
# Usage in FastAPI Application
# ============================================================================

"""
To integrate these secure endpoints into your FastAPI application:

1. Replace existing endpoints with secure versions:

app = FastAPI()

@app.post("/evaluate_answer")
async def evaluate_answer(
    request: QuestionSubmissionRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    return await secure_evaluate_answer(request, http_request, db)

@app.get("/api/bookmarks")
async def get_bookmarks(
    http_request: Request,
    db: Session = Depends(get_db),
    filters: FilterRequest = Depends(),
    pagination: PaginationRequest = Depends()
):
    return await secure_get_bookmarks(http_request, db, filters, pagination)

@app.post("/ide/execute")
async def execute_code(
    request: CodeExecutionRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    return await secure_execute_code(request, http_request, db)

2. Add security middleware for logging:

@app.middleware("http")
async def security_logging_middleware(request: Request, call_next):
    # Log all requests
    logger.info(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Log security events
    if response.status_code >= 400:
        logger.warning(f"Failed request: {request.method} {request.url.path} - {response.status_code}")
    
    return response

3. Enable CORS with restrictions:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

4. Add rate limiting (using slowapi or similar):

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/submit")
@limiter.limit("10/minute")
async def submit_endpoint(request: Request):
    # Your endpoint logic
    pass
"""
