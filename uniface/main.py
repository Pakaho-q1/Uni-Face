import sys
import os
import argparse
import uvicorn

from uniface.core.state import state
from uniface.core.model_manager import install_models

def main():
    parser = argparse.ArgumentParser(description="Uni-Face: Unified Face Processing Suite")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Serve / WebUI
    serve_parser = subparsers.add_parser("serve", help="Start the Uni-Face API & WebUI server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to run the API server on")
    serve_parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address to bind to")
    
    # Models
    models_parser = subparsers.add_parser("models", help="Model management commands")
    models_parser.add_argument("subcommand", choices=["install"], help="Models subcommand (e.g. install)")
    models_parser.add_argument("--force", action="store_true", help="Force redownload all models")
    
    args = parser.parse_args()
    
    if args.command == "serve":
        state.init(parse_args=False)
        print(f"Starting Uni-Face WebUI on {args.host}:{args.port}...")
        uvicorn.run("uniface.api_server:app", host=args.host, port=args.port, reload=False)
    elif args.command == "models":
        if args.subcommand == "install":
            install_models(force=args.force)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
