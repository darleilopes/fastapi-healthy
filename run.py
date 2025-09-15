#!/usr/bin/env python3
"""
Script to execute the FastAPI Healthy application.

This script is used to execute the FastAPI Healthy application.
"""

import os
import sys
import argparse
from pathlib import Path

# Adds the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir.parent))

from app.config.settings import settings


def main():
    """Main function to execute the FastAPI Healthy application."""
    parser = argparse.ArgumentParser(description="Start FastAPI Healthy app")
    parser.add_argument(
        "--host",
        default=settings.host,
        help=f"Host to bind (default: {settings.host})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.port,
        help=f"Port to bind (default: {settings.port})"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)"
    )
    parser.add_argument(
        "--log-level",
        choices=["critical", "error", "warning", "info", "debug"],
        default="info",
        help="Log level (default: info)"
    )
    
    args = parser.parse_args()
    
    try:
        import uvicorn
        
        print(f"Starting {settings.app_name} v{settings.app_version}")
        print(f"Environment: {settings.environment}")
        print(f"Server: http://{args.host}:{args.port}")
        print(f"Docs: http://{args.host}:{args.port}/docs")
        print(f"Healty: http://{args.host}:{args.port}/healthz")
        print(f"Metrics: http://{args.host}:{args.port}/metrics")
        print("-" * 50)
        
        uvicorn.run(
            "app.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers,
            log_level=args.log_level,
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
    except ImportError:
        print("Error: uvicorn not installed. Install dependencies with: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
