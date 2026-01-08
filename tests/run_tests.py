#!/usr/bin/env python3
"""
Test runner that handles imports properly
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import test modules directly
from tests.test_config import TestConfig
from tests.test_utils_simple import TestUtilsSimple
from tests.test_processor_simple import TestImageProcessorSimple
from tests.test_batch_simple import TestBatchProcessorSimple
from tests.test_cli_simple import TestCLISimple
from tests.test_minimal_cli import TestMinimalCLI


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilsSimple))
    suite.addTests(loader.loadTestsFromTestCase(TestImageProcessorSimple))
    suite.addTests(loader.loadTestsFromTestCase(TestBatchProcessorSimple))
    suite.addTests(loader.loadTestsFromTestCase(TestCLISimple))
    suite.addTests(loader.loadTestsFromTestCase(TestMinimalCLI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)