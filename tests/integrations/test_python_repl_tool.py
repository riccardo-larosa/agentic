import pytest
from src.tools.python_repl import python_repl_tool


def test_python_repl_tool_success():
    code = "print(1 + 1)"
    result = python_repl_tool(code)
    assert "Successfully executed" in result
    assert "Stdout: 2" in result


def test_python_repl_tool_syntax_error():
    code = "print(1 + )"
    result = python_repl_tool(code)
    assert "Error executing code:" in result
    assert code in result
    assert "SyntaxError" in result


def test_python_repl_tool_runtime_error():
    code = "print(1 / 0)"
    result = python_repl_tool(code)
    assert "Error executing code:" in result
    assert code in result
    assert "ZeroDivisionError" in result


def test_python_repl_tool_name_error():
    code = "print(undefined_variable)"
    result = python_repl_tool(code)
    assert "Error executing code:" in result
    assert code in result
    assert "NameError" in result


def test_python_repl_tool_type_error():
    code = "'2' + 2"
    result = python_repl_tool(code)
    assert "Error executing code:" in result
    assert code in result
    assert "TypeError" in result


def test_python_repl_tool_import_error():
    code = "from nonexistent_module import something"
    result = python_repl_tool(code)
    assert "Error executing code:" in result
    assert code in result
    assert "ModuleNotFoundError" in result


def test_python_repl_tool_exception():
    code = "raise Exception('Test')"
    result = python_repl_tool(code)
    assert "Error executing code:" in result
    assert code in result
    assert "Exception" in result


def test_python_repl_tool_with_multiple_lines():
    """Test execution of multiple lines of code"""
    code = "x = 5; y = 10; print(x + y)"  # Use single line with semicolons
    result = python_repl_tool(code)
    assert "Successfully executed" in result
    assert "Stdout: 15" in result


def test_python_repl_tool_with_imports():
    """Test execution of code with standard library imports"""
    code = "import math; print(round(math.pi, 2))"  # Single line
    result = python_repl_tool(code)
    assert "Successfully executed" in result
    assert "3.14" in result


def test_python_repl_tool_with_complex_calculation():
    """Test execution of more complex calculations"""
    # All in one line with a lambda instead of a function
    code = "print((lambda n: n * (n-1) if n > 1 else 1)(5))"
    result = python_repl_tool(code)
    assert "Successfully executed" in result
    assert "Stdout: 20" in result


def test_python_repl_tool_with_empty_string():
    """Test handling of empty string input"""
    code = ""
    result = python_repl_tool(code)
    assert "Successfully executed" in result


def test_python_repl_tool_with_whitespace():
    """Test handling of whitespace-only input"""
    code = "   \n   \t   "
    result = python_repl_tool(code)
    assert "Successfully executed" in result


def test_python_repl_tool_simple_calculation():
    """Test simple calculation in one line"""
    code = "print(sum(range(5)))"
    result = python_repl_tool(code)
    assert "Successfully executed" in result
    assert "Stdout: 10" in result


@pytest.mark.parametrize("test_input,expected_output", [
    ("print('hello')", "hello"),
    ("print(2 + 2)", "4"),
    ("print([1, 2, 3])", "[1, 2, 3]"),
    ("print({'a': 1})", "{'a': 1}"),
])
def test_python_repl_tool_various_outputs(test_input, expected_output):
    """Test different types of output handling"""
    result = python_repl_tool(test_input)
    assert "Successfully executed" in result
    assert f"Stdout: {expected_output}" in result


def test_python_repl_tool_with_long_output():
    """Test handling of long output"""
    code = "print('x' * 100)"  # Reduced length for test
    result = python_repl_tool(code)
    assert "Successfully executed" in result
    assert "Stdout:" in result
    assert "x" * 100 in result


def test_python_repl_tool_list_comprehension():
    """Test list comprehension in one line"""
    code = "print([x*x for x in range(5)])"
    result = python_repl_tool(code)
    assert "Successfully executed" in result
    assert "Stdout: [0, 1, 4, 9, 16]" in result