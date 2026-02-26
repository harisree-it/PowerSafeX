"""
Tests Package

This package contains all test sequences for the power converter test automation system.
Each test is implemented as a separate class inheriting from BaseTest.
"""

from .base_test import BaseTest
from .test_01_input_voltage_range import InputVoltageRangeTest
from .test_02_output_voltage_accuracy import OutputVoltageAccuracyTest

# Test registry mapping test names to test classes
TEST_REGISTRY = {
    "Input voltage range verification": InputVoltageRangeTest,
    "Output voltage accuracy": OutputVoltageAccuracyTest,
    # Add more tests as they are implemented
}

def get_test_class(test_name):
    """
    Get the test class for a given test name
    
    Args:
        test_name: Name of the test
        
    Returns:
        Test class or None if not found
    """
    return TEST_REGISTRY.get(test_name)

__all__ = [
    'BaseTest',
    'InputVoltageRangeTest',
    'OutputVoltageAccuracyTest',
    'TEST_REGISTRY',
    'get_test_class'
]
