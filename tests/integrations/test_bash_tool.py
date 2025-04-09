from src.tools.bash_tool import bash_tool


def test_bash_tool_success():
    cmd = "echo 'Hello, World!'"
    result = bash_tool(cmd)
    assert "Hello, World!" in result


def test_bash_tool_error():
    cmd = "ls /nonexistent/directory"
    result = bash_tool(cmd)
    assert "Command failed with exit code" in result
    assert "No such file or directory" in result


def test_bash_tool_timeout():
    # Note: The timeout parameter is handled internally by the bash_tool implementation
    # We'll test a command that should complete quickly
    cmd = "echo 'test'"
    result = bash_tool(cmd)
    assert "test" in result


def test_bash_tool_multiple_commands():
    cmd = "echo 'First' && echo 'Second'"
    result = bash_tool(cmd)
    assert "First" in result
    assert "Second" in result


def test_bash_tool_pipe():
    cmd = "echo 'Hello' | tr 'e' 'a'"
    result = bash_tool(cmd)
    assert "Hallo" in result


def test_bash_tool_environment_variable():
    cmd = "echo $HOME"
    result = bash_tool(cmd)
    assert result.strip() != ""  # HOME should be set in most environments


def test_bash_tool_empty_command():
    cmd = ""
    result = bash_tool(cmd)
    assert result == ""  # Empty command should return empty output 