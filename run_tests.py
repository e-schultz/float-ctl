#!/usr/bin/env python3
"""
FLOAT Test Runner
=================

Convenient script to run FLOAT tests with various options.
Provides easy access to different test categories and reporting options.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle output"""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(description="FLOAT Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--config", action="store_true", help="Run configuration tests only")
    parser.add_argument("--daemon", action="store_true", help="Run daemon tests only")
    parser.add_argument("--patterns", action="store_true", help="Run pattern detection tests only")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage reporting")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--fast", action="store_true", help="Skip slow tests")
    parser.add_argument("--file", help="Run specific test file")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies")
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("📦 Installing test dependencies...")
        install_cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"]
        if not run_command(install_cmd, "Installing test dependencies"):
            return 1
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Add coverage
    if args.coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term-missing"])
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(["-n", "auto"])
    
    # Add test filtering
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.config:
        cmd.extend(["-m", "config"])
    elif args.daemon:
        cmd.extend(["-m", "daemon"])
    elif args.patterns:
        cmd.extend(["-m", "patterns"])
    
    # Skip slow tests if requested
    if args.fast:
        cmd.extend(["-m", "not slow"])
    
    # Run specific file if requested
    if args.file:
        cmd.append(args.file)
    
    # Add default test directory if no specific file
    if not args.file:
        cmd.append("tests/")
    
    # Run the tests
    success = run_command(cmd, "Running FLOAT tests")
    
    # Show coverage report location if coverage was enabled
    if args.coverage and success:
        coverage_dir = Path("htmlcov")
        if coverage_dir.exists():
            print(f"\n📊 Coverage report generated at: {coverage_dir.absolute()}/index.html")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())