import argparse
import sys
from uniface.cli.adapter import run_cli
from uniface.api.adapter import run_server

def main():
    parser = argparse.ArgumentParser(description="Uni-Face: Faceswap Project", add_help=False)
    # We parse command
    parser.add_argument("command", choices=["cli", "serve", "models"], help="Command to run")
    
    # Parse known args so we don't error out on CLI flags meant for the adapter
    args, unknown = parser.parse_known_args(sys.argv[1:2])
    
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "cli":
        run_cli()
    elif args.command == "serve":
        from uniface.core.state import state
        state.init(parse_args=False)
        serve_parser = argparse.ArgumentParser(prog="main.py serve")
        serve_parser.add_argument("--port", type=int, default=state.server_port, help="Port to run the API server on")
        serve_args = serve_parser.parse_args(sys.argv[2:])
        run_server(port=serve_args.port)
    elif args.command == "models":
        models_parser = argparse.ArgumentParser(prog="main.py models")
        models_parser.add_argument("subcommand", choices=["install"], help="Models subcommand (e.g. install)")
        models_parser.add_argument("--force", action="store_true", help="Force redownload all models")
        models_args = models_parser.parse_args(sys.argv[2:])
        
        if models_args.subcommand == "install":
            from uniface.core.model_manager import install_models
            install_models(force=models_args.force)

if __name__ == "__main__":
    main()
