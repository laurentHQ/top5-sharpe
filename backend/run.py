#!/usr/bin/env python3
"""
FastAPI Application Runner

Simple script to run the FastAPI application with proper configuration.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn
from backend.app.core.config import settings


def main():
    """Main entry point for running the FastAPI application"""
    print(f"Starting {settings.TITLE} v{settings.VERSION}")
    print(f"Environment: {settings.environment}")
    print(f"Server will start on http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()