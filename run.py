#!/usr/bin/env python3
"""
Directory Mapper - Main entry point

This script can run either the CLI or GUI version of the directory mapper.
Usage:
    python run.py          # Run GUI version
    python run.py cli      # Run CLI version
    python run.py --help   # Show help
"""

import sys
import os

def show_help():
    print("Directory Mapper - Generate text-based directory structure maps")
    print()
    print("Usage:")
    print("    python run.py          # Run GUI version (default)")
    print("    python run.py gui      # Run GUI version")
    print("    python run.py cli      # Run CLI version")
    print("    python run.py --help   # Show this help")
    print()
    print("GUI Features:")
    print("  - Browse and select directories with file dialog")
    print("  - Optional .gitignore exclusion with checkbox")
    print("  - Live preview of directory structure")
    print("  - Save output to custom file location")
    print()
    print("CLI Features:")
    print("  - Command-line interface for batch processing")
    print("  - Saves output to directory_map.txt in current directory")

def run_gui():
    try:
        from directory_mapper_gui import main
        main()
    except ImportError as e:
        print(f"Error: Could not import GUI components: {e}")
        print("Make sure tkinter is installed: sudo apt install python3-tk")
        sys.exit(1)

def run_cli():
    # Import and run the original CLI functionality
    os.system(f"{sys.executable} dirmap.py")

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--help', '-h', 'help']:
            show_help()
        elif arg == 'cli':
            run_cli()
        elif arg == 'gui':
            run_gui()
        else:
            print(f"Unknown argument: {arg}")
            show_help()
            sys.exit(1)
    else:
        # Default to GUI
        run_gui()

if __name__ == "__main__":
    main()