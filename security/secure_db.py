"""
Secure Database Query Builder
Prevents SQL injection through parameterized queries and input validation
"""

from typing import Any, Dict, List, Optional, Union
from sqlalchemy import and_, or_, text
from sqlalchemy.orm import Query, Session
import logging

logger = logging.getLogger(__name__)


class SecureQueryBuilder:
    """Build secure database queries with automatic parameterization"""
    
    # Allowed operators for filtering
    ALLOWED_OPERATORS = {
        'eq': '=',
        'ne': '!=',
        'gt': '>',
        'gte': '>=',
        'lt': '<',
        'lte': '<=',
        'like': 'LIKE',
        'ilike': 'ILIKE',
        'in': 'IN',
        'not_in': 'NOT IN',
    }
    
    # Allowed sort orders
    ALLOWED_ORDERS = {'asc', 'desc'}
    
    @staticmethod
    def validate_column_name(column: str, allowed_columns: List[str]) -> bool:
        """
        Validate that column name is in allowed list
        Prevents SQL injection through column names
        """
        return column in allowed_columns
    
    @staticmethod
    def build_filter(model, filters: Dict[str, Any], allowed_columns: List[str]) -> List:
        """
        Build secure filter conditions
        
        Args:
            model: SQLAlchemy model class
            filters: Dictionary of filters {column: value} or {column: {operator: value}}
            allowed_columns: List of allowed column names
            
        Returns:
            List of SQLAlchemy filter conditions
        """
        conditions = []
        
        for column, value in filters.items():
            # Validate column name
            if not SecureQueryBuilder.validate_column_name(column, allowed_columns):
                logger.warning(f"Attempted to filter on disallowed column: {column}")
                continue
            
            # Get column attribute
            if not hasattr(model, column):
                logger.warning(f"Column {column} not found on model {model.__name__}")
                continue
            
            col_attr = getattr(model, column)
            
            # Handle different filter formats
            if isinstance(value, dict):
                # Format: {column: {operator: value}}
                for op, op_value in value.items():
                    if op not in SecureQueryBuilder.ALLOWED_OPERATORS:
                        logger.warning(f"Invalid operator: {op}")
                        continue
                    
                    if op == 'eq':
                        conditions.append(col_attr == op_value)
                    elif op == 'ne':
                        conditions.append(col_attr != op_value)
                    elif op == 'gt':
                        conditions.append(col_attr > op_value)
                    elif op == 'gte':
                        conditions.append(col_attr >= op_value)
                    elif op == 'lt':
                        conditions.append(col_attr < op_value)
                    elif op == 'lte':
                        conditions.append(col_attr <= op_value)
                    elif op == 'like':
                        conditions.append(col_attr.like(op_value))
                    elif op == 'ilike':
                        conditions.append(col_attr.ilike(op_value))
                    elif op == 'in':
                        conditions.append(col_attr.in_(op_value))
                    elif op == 'not_in':
                        conditions.append(~col_attr.in_(op_value))
            else:
                # Simple equality filter
                conditions.append(col_attr == value)
        
        return conditions
    
    @staticmethod
    def apply_pagination(query: Query, page: int = 1, limit: int = 10, max_limit: int = 100) -> Query:
        """
        Apply pagination to query with validation
        
        Args:
            query: SQLAlchemy query
            page: Page number (1-indexed)
            limit: Items per page
            max_limit: Maximum allowed limit
            
        Returns:
            Paginated query
        """
        # Validate and sanitize inputs
        page = max(1, int(page))
        limit = max(1, min(int(limit), max_limit))
        
        offset = (page - 1) * limit
        
        return query.offset(offset).limit(limit)
    
    @staticmethod
    def apply_sorting(query: Query, model, sort_by: str, order: str, allowed_columns: List[str]) -> Query:
        """
        Apply sorting to query with validation
        
        Args:
            query: SQLAlchemy query
            model: SQLAlchemy model class
            sort_by: Column to sort by
            order: Sort order ('asc' or 'desc')
            allowed_columns: List of allowed column names
            
        Returns:
            Sorted query
        """
        # Validate column
        if not SecureQueryBuilder.validate_column_name(sort_by, allowed_columns):
            logger.warning(f"Attempted to sort by disallowed column: {sort_by}")
            return query
        
        # Validate order
        order = order.lower()
        if order not in SecureQueryBuilder.ALLOWED_ORDERS:
            logger.warning(f"Invalid sort order: {order}")
            order = 'asc'
        
        # Get column attribute
        if not hasattr(model, sort_by):
            logger.warning(f"Column {sort_by} not found on model {model.__name__}")
            return query
        
        col_attr = getattr(model, sort_by)
        
        # Apply sorting
        if order == 'desc':
            return query.order_by(col_attr.desc())
        else:
            return query.order_by(col_attr.asc())
    
    @staticmethod
    def safe_search(query: Query, model, search_term: str, search_columns: List[str]) -> Query:
        """
        Apply safe full-text search across multiple columns
        
        Args:
            query: SQLAlchemy query
            model: SQLAlchemy model class
            search_term: Search term (will be sanitized)
            search_columns: List of columns to search in
            
        Returns:
            Query with search filters
        """
        if not search_term or not search_columns:
            return query
        
        # Sanitize search term
        search_term = search_term.strip()
        if not search_term:
            return query
        
        # Escape special characters for LIKE
        search_term = search_term.replace('%', '\\%').replace('_', '\\_')
        search_pattern = f"%{search_term}%"
        
        # Build OR conditions for each search column
        search_conditions = []
        for column in search_columns:
            if hasattr(model, column):
                col_attr = getattr(model, column)
                search_conditions.append(col_attr.ilike(search_pattern))
        
        if search_conditions:
            query = query.filter(or_(*search_conditions))
        
        return query


class SecureDBOperations:
    """Secure database operations with input validation"""
    
    @staticmethod
    def safe_get_by_id(db: Session, model, record_id: int, user_id: int = None) -> Optional[Any]:
        """
        Safely get record by ID with optional user ownership check
        
        Args:
            db: Database session
            model: SQLAlchemy model class
            record_id: Record ID
            user_id: Optional user ID for ownership check
            
        Returns:
            Record or None
        """
        try:
            record_id = int(record_id)
            
            query = db.query(model).filter(model.id == record_id)
            
            # Add user ownership check if provided
            if user_id is not None and hasattr(model, 'user_id'):
                query = query.filter(model.user_id == int(user_id))
            
            return query.first()
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid ID format: {e}")
            return None
    
    @staticmethod
    def safe_create(db: Session, model, data: Dict[str, Any], allowed_fields: List[str]) -> Optional[Any]:
        """
        Safely create record with field validation
        
        Args:
            db: Database session
            model: SQLAlchemy model class
            data: Data dictionary
            allowed_fields: List of allowed field names
            
        Returns:
            Created record or None
        """
        try:
            # Filter to only allowed fields
            filtered_data = {k: v for k, v in data.items() if k in allowed_fields}
            
            # Create record
            record = model(**filtered_data)
            db.add(record)
            db.flush()
            
            return record
        except Exception as e:
            logger.error(f"Error creating record: {e}")
            db.rollback()
            return None
    
    @staticmethod
    def safe_update(db: Session, model, record_id: int, data: Dict[str, Any], 
                   allowed_fields: List[str], user_id: int = None) -> Optional[Any]:
        """
        Safely update record with field validation
        
        Args:
            db: Database session
            model: SQLAlchemy model class
            record_id: Record ID
            data: Update data dictionary
            allowed_fields: List of allowed field names
            user_id: Optional user ID for ownership check
            
        Returns:
            Updated record or None
        """
        try:
            # Get record
            record = SecureDBOperations.safe_get_by_id(db, model, record_id, user_id)
            if not record:
                return None
            
            # Filter to only allowed fields
            filtered_data = {k: v for k, v in data.items() if k in allowed_fields}
            
            # Update fields
            for key, value in filtered_data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            
            db.flush()
            return record
        except Exception as e:
            logger.error(f"Error updating record: {e}")
            db.rollback()
            return None
    
    @staticmethod
    def safe_delete(db: Session, model, record_id: int, user_id: int = None) -> bool:
        """
        Safely delete record with ownership check
        
        Args:
            db: Database session
            model: SQLAlchemy model class
            record_id: Record ID
            user_id: Optional user ID for ownership check
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            # Get record
            record = SecureDBOperations.safe_get_by_id(db, model, record_id, user_id)
            if not record:
                return False
            
            db.delete(record)
            db.flush()
            return True
        except Exception as e:
            logger.error(f"Error deleting record: {e}")
            db.rollback()
            return False
    
    @staticmethod
    def safe_count(db: Session, model, filters: Dict[str, Any] = None, 
                  allowed_columns: List[str] = None) -> int:
        """
        Safely count records with filters
        
        Args:
            db: Database session
            model: SQLAlchemy model class
            filters: Optional filters
            allowed_columns: List of allowed column names for filtering
            
        Returns:
            Count of records
        """
        try:
            query = db.query(model)
            
            if filters and allowed_columns:
                conditions = SecureQueryBuilder.build_filter(model, filters, allowed_columns)
                if conditions:
                    query = query.filter(and_(*conditions))
            
            return query.count()
        except Exception as e:
            logger.error(f"Error counting records: {e}")
            return 0


# Export main classes
__all__ = ['SecureQueryBuilder', 'SecureDBOperations']
