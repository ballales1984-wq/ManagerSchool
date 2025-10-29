"""
Test runner principale - esegue tutti i test.
"""

import pytest
import sys


def main():
    """Esegue tutti i test."""
    print("=" * 70)
    print("TEST SUITE MANAGERSCHOOL")
    print("=" * 70)
    print()
    
    # Esegui tutti i test
    exit_code = pytest.main([
        "-v",
        "--tb=short",
        "--cov=.",
        "--cov-report=term",
        "--cov-report=html",
        "-m", "not slow"
    ])
    
    if exit_code == 0:
        print()
        print("=" * 70)
        print("TUTTI I TEST PASSATI!")
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("ALCUNI TEST FALLITI")
        print("=" * 70)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

