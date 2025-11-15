"""Web scraping utility for research agent."""
import requests
from bs4 import BeautifulSoup
from typing import Optional


class WebScraper:
    """Scrapes and extracts content from web articles."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_article(self, url: str) -> Optional[dict]:
        """
        Scrape article content from a URL.

        Args:
            url: The URL to scrape

        Returns:
            Dictionary with title and content, or None if failed
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()

            # Try to find title
            title = None
            if soup.find('h1'):
                title = soup.find('h1').get_text().strip()
            elif soup.find('title'):
                title = soup.find('title').get_text().strip()

            # Extract main content
            # Try common article containers
            main_content = None
            for selector in ['article', 'main', '.post-content', '.article-content', '.content']:
                if isinstance(selector, str) and selector.startswith('.'):
                    content = soup.find(class_=selector.replace('.', ''))
                else:
                    content = soup.find(selector)

                if content:
                    main_content = content
                    break

            # Fallback to body if no article container found
            if not main_content:
                main_content = soup.find('body')

            if main_content:
                # Extract text with some structure preserved
                paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li'])
                content_text = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            else:
                content_text = soup.get_text()

            # Clean up whitespace
            content_text = '\n'.join([line.strip() for line in content_text.split('\n') if line.strip()])

            return {
                'title': title or 'No title found',
                'content': content_text,
                'url': url
            }

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
