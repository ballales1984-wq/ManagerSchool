#!/usr/bin/env python3
"""
Script per eseguire tutti i test del progetto.
"""

import unittest
import sys


def run_all_tests():
    """Esegue tutti i test e mostra risultati."""
    
    print("="*80)
    print("🧪 REGISTRO SCOLASTICO INTELLIGENTE - TEST SUITE".center(80))
    print("="*80)
    print()
    
    # Discover e esegui test
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Risultati
    print()
    print("="*80)
    
    if result.wasSuccessful():
        print("✅ TUTTI I TEST PASSATI!".center(80))
    else:
        print("❌ ALCUNI TEST FALLITI".center(80))
    
    print("="*80)
    print(f"\nTest eseguiti: {result.testsRun}")
    print(f"Errori: {len(result.errors)}")
    print(f"Fallimenti: {len(result.failures)}")
    print(f"Saltati: {len(result.skipped)}")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())

