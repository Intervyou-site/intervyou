#!/usr/bin/env python3
"""
Training entrypoint for the ML models
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipelines.training_pipeline import TrainingPipeline
from src.utils import load_config

def main():
    """Main training function"""
    config = load_config()
    pipeline = TrainingPipeline(config)
    pipeline.run()

if __name__ == "__main__":
    main()