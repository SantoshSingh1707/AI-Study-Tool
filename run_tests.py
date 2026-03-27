#!/usr/bin/env python3
"""
Comprehensive test runner for the entire project.
Runs both backend (Python) and frontend (TypeScript) tests.

Usage:
    python run_tests.py [--backend] [--frontend] [--coverage] [--watch]
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, cwd=None, capture_output=False):
    """Run a shell command and return result"""
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}\n")

    result = subprocess.run(
        cmd,
        cwd=cwd or Path.cwd(),
        capture_output=capture_output,
        text=True
    )

    if capture_output:
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

    return result.returncode


def run_backend_tests(coverage=False, watch=False):
    """Run backend Python tests"""
    print("\n" + "="*60)
    print("🔵 BACKEND TESTS (Python)")
    print("="*60)

    cwd = Path("backend")

    # Install test dependencies if needed
    if not (cwd / "venv").exists():
        print("⚠️  Virtual environment not found. Using system Python...")

    cmd = ["pytest", "tests/"]
    if coverage:
        cmd = ["pytest", "tests/", "--cov=src", "--cov-report=html", "--cov-report=term"]
    if watch:
        cmd = ["ptw", "tests/"]  # Requires pytest-watch

    return run_command(cmd, cwd=cwd)


def run_frontend_tests(coverage=False, watch=False):
    """Run frontend TypeScript tests"""
    print("\n" + "="*60)
    print("🟢 FRONTEND TESTS (TypeScript)")
    print("="*60)

    cwd = Path("frontend")

    if not (cwd / "node_modules").exists():
        print("❌ node_modules not found. Run 'npm install' first!")
        return 1

    cmd = ["npm", "test", "--", "--run"]
    if coverage:
        cmd = ["npm", "run", "test:coverage"]
    if watch:
        cmd = ["npm", "test"]

    return run_command(cmd, cwd=cwd)


def main():
    parser = argparse.ArgumentParser(description="Run all tests")
    parser.add_argument("--backend", action="store_true", help="Run only backend tests")
    parser.add_argument("--frontend", action="store_true", help="Run only frontend tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage reports")
    parser.add_argument("--watch", action="store_true", help="Watch mode for development")
    args = parser.parse_args()

    results = {}

    # Determine which tests to run
    run_backend = args.backend or not args.frontend
    run_frontend = args.frontend or not args.backend

    # Run backend tests
    if run_backend:
        results['backend'] = run_backend_tests(args.coverage, args.watch)

    # Run frontend tests
    if run_frontend:
        results['frontend'] = run_frontend_tests(args.coverage, args.watch)

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    for name, code in results.items():
        status = "✅ PASSED" if code == 0 else "❌ FAILED"
        print(f"{name}: {status} (exit code: {code})")

    overall = 0 if all(c == 0 for c in results.values()) else 1

    print(f"\nOverall: {'✅ ALL PASSED' if overall == 0 else '❌ SOME FAILED'}")
    print("="*60 + "\n")

    if args.coverage:
        print("\n📈 Coverage Reports Generated:")
        if run_backend:
            print("  - Backend: backend/htmlcov/index.html")
        if run_frontend:
            print("  - Frontend: frontend/coverage/index.html")

    sys.exit(overall)


if __name__ == "__main__":
    main()
