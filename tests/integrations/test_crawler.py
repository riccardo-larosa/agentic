import pytest
from unittest.mock import MagicMock, patch
from src.crawler.crawler import Crawler
from src.crawler.article import Article


@pytest.fixture
def sample_html():
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Test Article</h1>
            <p>This is a test paragraph.</p>
            <img src="test.jpg" alt="test image">
        </body>
    </html>
    """


@pytest.fixture
def mock_jina_client():
    with patch('src.crawler.crawler.JinaClient') as mock:
        instance = mock.return_value
        instance.crawl.return_value = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Test Article</h1>
                <p>This is a test paragraph.</p>
            </body>
        </html>
        """
        yield instance


@pytest.fixture
def mock_readability_extractor():
    with patch('src.crawler.crawler.ReadabilityExtractor') as mock:
        instance = mock.return_value
        article = Article("Test Article", "<h1>Test Article</h1><p>This is a test paragraph.</p>")
        instance.extract_article.return_value = article
        yield instance


def test_crawler_initialization():
    """Test Crawler class initialization"""
    crawler = Crawler()
    assert isinstance(crawler, Crawler)


def test_crawler_crawl(mock_jina_client, mock_readability_extractor):
    """Test the crawl method with mocked dependencies"""
    crawler = Crawler()
    url = "https://example.com"
    article = crawler.crawl(url)
    
    # Verify JinaClient was called correctly
    mock_jina_client.crawl.assert_called_once_with(url, return_format="html")
    
    # Verify ReadabilityExtractor was called
    mock_readability_extractor.extract_article.assert_called_once()
    
    # Verify Article properties
    assert isinstance(article, Article)
    assert article.url == url
    assert article.title == "Test Article"


def test_crawler_with_real_url():
    """Test the crawler with a real URL (integration test)"""
    crawler = Crawler()
    url = "https://example.com"  # Using a stable test URL
    article = crawler.crawl(url)
    
    assert isinstance(article, Article)
    assert article.url == url
    assert article.title is not None
    assert article.html_content is not None


@pytest.mark.parametrize("test_url", [
    "https://example.com",
    "http://test.com",
    "https://subdomain.example.com/path?query=test"
])
def test_crawler_with_different_urls(test_url, mock_jina_client, mock_readability_extractor):
    """Test the crawler with different URL formats"""
    crawler = Crawler()
    article = crawler.crawl(test_url)
    
    assert isinstance(article, Article)
    assert article.url == test_url


def test_crawler_error_handling():
    """Test crawler error handling with invalid URL"""
    crawler = Crawler()
    with pytest.raises(Exception):  # Adjust the exception type based on your error handling
        crawler.crawl("invalid-url")


def test_main_function(mock_jina_client, mock_readability_extractor):
    """Test the main function with command line arguments"""
    with patch('sys.argv', ['crawler.py', 'https://example.com']):
        crawler = Crawler()
        article = crawler.crawl('https://example.com')
        assert isinstance(article, Article)
        assert article.url == 'https://example.com'