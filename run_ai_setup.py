#!/usr/bin/env python3
"""
Enhanced wrapper to run AI setup with proper encoding
"""

import subprocess
import sys
import os

def run_setup():
    """Run the AI setup with proper encoding"""
    
    print("=== Disaster Management AI Setup ===")
    print("=" * 40)
    
    # Check if src directory exists
    src_dir = "src"
    if not os.path.exists(src_dir):
        print(f"ERROR: 'src' directory not found in {os.getcwd()}")
        return False
    
    # Check if setup_ai.py exists in src directory
    setup_path = os.path.join(src_dir, "setup_ai.py")
    if not os.path.exists(setup_path):
        print(f"ERROR: setup_ai.py not found in {src_dir}/")
        print("Files in src/:", os.listdir(src_dir) if os.path.exists(src_dir) else "Directory not found")
        return False
    
    print(f"Found setup script: {setup_path}")
    
    try:
        # Change to src directory
        original_dir = os.getcwd()
        os.chdir(src_dir)
        print(f"Changed to directory: {os.getcwd()}")
        
        # Build command based on platform
        cmd = [sys.executable]
        
        if sys.platform == "win32":
            print("Windows detected - using UTF-8 encoding...")
            cmd.extend(["-X", "utf8"])
        
        cmd.append("setup_ai.py")
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        # Print the output
        print(result.stdout)
        
        if result.stderr:
            print("\n=== ERRORS ===")
            print(result.stderr)
        
        # Change back to original directory
        os.chdir(original_dir)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Failed to run setup: {e}")
        # Ensure we change back to original directory even if there's an error
        try:
            os.chdir(original_dir)
        except:
            pass
        return False

def main():
    success = run_setup()
    
    if success:
        print("\n" + "=" * 40)
        print("SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 40)
    else:
        print("\n" + "=" * 40)
        print("SETUP FAILED!")
        print("=" * 40)
        sys.exit(1)

if __name__ == "__main__":
    main()