import pytest
from src.crawler.article import Article


def test_article_initialization():
    """Test Article class initialization"""
    title = "Test Title"
    html_content = "<p>Test content</p>"
    article = Article(title, html_content)
    assert article.title == title
    assert article.html_content == html_content


def test_to_markdown_with_title():
    """Test conversion to markdown with title"""
    article = Article("Test Title", "<p>Test content</p>")
    markdown = article.to_markdown(including_title=True)
    assert "# Test Title" in markdown
    assert "Test content" in markdown


def test_to_markdown_without_title():
    """Test conversion to markdown without title"""
    article = Article("Test Title", "<p>Test content</p>")
    markdown = article.to_markdown(including_title=False)
    assert "# Test Title" not in markdown
    assert "Test content" in markdown


def test_to_message_text_only():
    """Test conversion to message format with text only"""
    article = Article("Test Title", "<p>Test content</p>")
    article.url = "http://example.com"
    message = article.to_message()
    assert len(message) == 1
    assert message[0]["type"] == "text"
    assert "Test content" in message[0]["text"]


def test_to_message_with_image():
    """Test conversion to message format with image"""
    html_content = """
    <p>Text before image</p>
    <img src="test.jpg" alt="test">
    <p>Text after image</p>
    """
    article = Article("Test Title", html_content)
    article.url = "http://example.com"
    message = article.to_message()
    
    # Verify we have multiple parts (text and image)
    assert len(message) > 1
    
    # Verify we have both text and image parts
    message_types = [m["type"] for m in message]
    assert "text" in message_types
    assert "image_url" in message_types
    
    # Verify image URL is properly joined with base URL
    image_messages = [m for m in message if m["type"] == "image_url"]
    assert any("http://example.com" in m["image_url"]["url"] for m in image_messages)


def test_to_message_without_url():
    """Test conversion to message format without setting URL"""
    article = Article("Test Title", "<img src='test.jpg'>")
    # URL is required for image processing
    with pytest.raises(AttributeError):
        article.to_message()


def test_complex_html_conversion():
    """Test conversion of complex HTML with nested elements"""
    html_content = """
    <div>
        <h1>Section 1</h1>
        <p>Paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </div>
    """
    article = Article("Complex Test", html_content)
    markdown = article.to_markdown()
    
    # Check for proper markdown conversion
    assert "**bold**" in markdown.lower() or "**bold**" in markdown
    assert "_italic_" in markdown.lower() or "*italic*" in markdown
    assert "- Item 1" in markdown or "* Item 1" in markdown