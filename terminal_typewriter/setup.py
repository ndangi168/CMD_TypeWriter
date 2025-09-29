#!/usr/bin/env python3
"""
Setup script for Terminal Typewriter
Handles installation, configuration, and initial setup
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")


def install_requirements():
    """Install required packages."""
    requirements_file = Path(__file__).parent / "requirements.txt"
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found")
        return False
    
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def setup_directories():
    """Create necessary directories."""
    base_dir = Path(__file__).parent
    directories = [
        base_dir / "data" / "database",
        base_dir / "data" / "texts",
        base_dir / "data" / "exports",
        base_dir / "config"
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    return True


def check_curses_support():
    """Check if curses is available."""
    print("🔍 Checking curses support...")
    try:
        import curses
        print("✅ Curses support available")
        return True
    except ImportError:
        print("⚠️  Curses not available - standard mode only")
        print("   Install 'windows-curses' on Windows for full functionality")
        return False


def verify_config_files():
    """Verify configuration files exist and are valid."""
    base_dir = Path(__file__).parent
    config_files = [
        base_dir / "config" / "default_settings.json",
        base_dir / "config" / "themes.json",
        base_dir / "config" / "achievements.json"
    ]
    
    print("⚙️  Verifying configuration files...")
    for config_file in config_files:
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    json.load(f)
                print(f"   ✅ {config_file.name}")
            except json.JSONDecodeError:
                print(f"   ⚠️  {config_file.name} - invalid JSON")
        else:
            print(f"   ❌ {config_file.name} - missing")
    
    return True


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("⚠️  Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Main setup function."""
    print("🎯 Terminal Typewriter Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_requirements():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create directories
    if not setup_directories():
        print("❌ Setup failed at directory creation")
        sys.exit(1)
    
    # Check curses support
    check_curses_support()
    
    # Verify config files
    verify_config_files()
    
    # Run tests
    if not run_tests():
        print("⚠️  Setup completed with test failures")
    else:
        print("✅ Setup completed successfully")
    
    print("\n🚀 Ready to start typing!")
    print("   Run: python main.py")
    print("\n📖 See README.md for usage instructions")


if __name__ == "__main__":
    main()
