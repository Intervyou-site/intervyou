"""
Utility functions for the ML project
"""
import yaml
import os
from typing import Dict, Any

def load_config(env: str = "local") -> Dict[str, Any]:
    """Load configuration from YAML files"""
    config_path = f"config/{env}.yaml"
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config

def setup_logging(config: Dict[str, Any]):
    """Setup logging configuration"""
    import logging
    
    logging.basicConfig(
        level=getattr(logging, config.get('logging', {}).get('level', 'INFO')),
        format=config.get('logging', {}).get('format', '%(asctime)s - %(levelname)s - %(message)s')
    )

def validate_input(data: Dict[str, Any], required_fields: list) -> bool:
    """Validate input data has required fields"""
    return all(field in data for field in required_fields)