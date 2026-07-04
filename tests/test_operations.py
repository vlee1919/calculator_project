import pytest

from app.operations import (OperationFactory, 
                            Addition, 
                            Subtraction, 
                            Multiplication, 
                            Division, 
                            Power, 
                            Root, 
                            Modulo,
                            IntegerDivision, 
                            Percentage, 
                            Absolute_diff)



class BaseOperationTest:

    def setup_method(self):
        self.factory = OperationFactory()

    def test_get_operation(self):

        operation = self.user_operation()
        for a, b, expected_result in self.user_inputs:
            result = operation.execute(a, b)
            assert result == expected_result, f"Expected {expected_result}, got {result}"

class Test_addition(BaseOperationTest):
    user_operation = Addition
    
    user_inputs = [
        (2, 3, 5),  # Test positive numbers
        (-1, 1, 0),  # Test negative result
        ]

class Test_subtraction(BaseOperationTest):
    user_operation = Subtraction
    
    user_inputs = [
        (5, 3, 2),  # Test positive result
        (3, 5, -2),  # Test negative result
        ]
            
class Test_multiplication(BaseOperationTest):
    user_operation = Multiplication
    
    user_inputs = [
        (4, 3, 12),  # Test positive numbers
        (-2, 3, -6),  # Test negative result
        ]

class Test_division(BaseOperationTest):
    user_operation = Division
    
    user_inputs = [
        (10, 2, 5),  # Test positive result
        ]
    
    """ Test for divide-by-zero error"""
    def test_division_by_zero(self):
        with pytest.raises(ValueError, match="Division by zero is not allowed."):
            self.user_operation().execute(10, 0)

class Test_root(BaseOperationTest):
    user_operation = Root
    
    user_inputs = [
        (4, 2, 2)
        ]
    """ Test for root-by-zero error"""
    def test_root_by_zero(self):
        with pytest.raises(ValueError, match="Zero root is undefined."):
            self.user_operation().execute(16, 0)

class Test_power(BaseOperationTest):
    user_operation = Power
    
    user_inputs = [
        (2, 3, 8),  
        (5, 0, 1),  
        ]

class Test_modulo(BaseOperationTest):
    user_operation = Modulo
    
    user_inputs = [
        (10, 3, 1),  
        (10, 5, 0),  
        ]
    """ Test for modulo-by-zero error"""
    def test_modulo_by_zero(self):
        with pytest.raises(ValueError, match="Modulo by zero is not allowed."):
            self.user_operation().execute(10, 0)

class Test_integer_division(BaseOperationTest):
    user_operation = IntegerDivision
    
    user_inputs = [
        (10, 3, 3),  
        (10, 5, 2),  
        ]
    """ Test for integer division-by-zero error"""
    def test_integer_division_by_zero(self):
        with pytest.raises(ValueError, match="Integer division by zero is not allowed."):
            self.user_operation().execute(10, 0)

class Test_percentage(BaseOperationTest):
    user_operation = Percentage
    
    user_inputs = [
        (200, 10, 20),  
        (150, 20, 30),  
        ]

class Test_absolute_diff(BaseOperationTest):
    user_operation = Absolute_diff
    
    user_inputs = [
        (5, 3, 2),  
        (3, 5, 2),  
        (10, 10, 0),  
        ]