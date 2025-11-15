"""Research agent for gathering information from web sources."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.web_scraper import WebScraper


class ResearchAgent:
    """Agent responsible for researching topics and gathering information."""

    def __init__(self, model: str = "gpt-5-mini-2025-08-07"):
        self.llm = ChatOpenAI(model=model, temperature=0.3)
        self.scraper = WebScraper()

        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research analyst for a CPA firm (FoxGlove CPA) specializing in tax planning
            and accounting for small businesses in Washington and Oregon.

            Your task is to analyze source material and extract key insights, statistics, and concepts
            that would be valuable for writing an article on the given topic.

            Focus on:
            - Key concepts and definitions
            - Specific numbers, percentages, or thresholds
            - Real-world examples or case studies
            - Common mistakes or pitfalls
            - Best practices
            - Regional considerations (especially WA/OR if relevant)

            Be thorough but concise. Organize your findings in a clear structure."""),
            ("user", """Topic: {topic}

            Source Material:
            {source_content}

            Please analyze this content and provide key insights for our article.""")
        ])

    def research_from_url(self, url: str, topic: str) -> Optional[str]:
        """
        Research a topic by scraping and analyzing a URL.

        Args:
            url: The URL to research
            topic: The topic we're researching for context

        Returns:
            Research findings as a string, or None if failed
        """
        print(f"🔍 Researching from URL: {url}")

        # Scrape the article
        article_data = self.scraper.scrape_article(url)

        if not article_data:
            return None

        print(f"✓ Scraped article: {article_data['title']}")

        # Analyze with LLM
        chain = self.analysis_prompt | self.llm

        result = chain.invoke({
            "topic": topic,
            "source_content": f"Title: {article_data['title']}\n\n{article_data['content'][:10000]}"  # Limit content length
        })

        return result.content

    def research_from_topic(self, topic: str, additional_context: str = "") -> str:
        """
        Research a topic without external sources, using the LLM's knowledge.

        Args:
            topic: The topic to research
            additional_context: Any additional context or requirements

        Returns:
            Research findings as a string
        """
        print(f"🔍 Researching topic: {topic}")

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research analyst for a CPA firm (FoxGlove CPA) specializing in tax planning
            and accounting for small businesses in Washington and Oregon.

            Your task is to provide comprehensive research on the given topic, drawing from your knowledge
            of accounting, tax law, and small business best practices.

            Focus on:
            - Key concepts and definitions
            - Specific numbers, percentages, or thresholds (especially current tax year)
            - Real-world examples or scenarios
            - Common mistakes or pitfalls
            - Best practices
            - Regional considerations (especially WA/OR differences)

            Organize your findings in a clear, structured format."""),
            ("user", """Topic: {topic}

            Additional Context: {context}

            Please provide comprehensive research on this topic.""")
        ])

        chain = prompt | self.llm
        result = chain.invoke({
            "topic": topic,
            "context": additional_context or "None provided"
        })

        return result.content
