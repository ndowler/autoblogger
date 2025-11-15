"""Writing agent for creating professional, approachable articles."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from typing import Optional


class WritingAgent:
    """Agent responsible for writing articles in a professional but approachable tone."""

    def __init__(self, model: str = "gpt-5-mini-2025-08-07"):
        self.llm = ChatOpenAI(model=model, temperature=0.7)

        self.writing_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional content writer for FoxGlove CPA, a CPA firm specializing in
            tax planning and accounting for small businesses in Washington and Oregon.

            Your writing style is:
            - Professional but approachable - like a knowledgeable friend explaining complex topics
            - Clear and practical - focus on actionable insights, not jargon
            - Conversational without being casual - use "you" and "we", occasional rhetorical questions
            - Example-driven - use real-world scenarios and numbers
            - Structured with clear headings and subheadings
            - Includes specific numbers, thresholds, and percentages when relevant
            - Addresses common questions and pain points directly

            Tone guidelines:
            - Start with a hook that addresses a common question or pain point
            - Use bold for emphasis on key points (sparingly)
            - Break complex topics into digestible sections
            - Include practical examples with specific dollar amounts
            - End sections with clear takeaways
            - Include a clear call-to-action at the end

            Format as MDX (Markdown with frontmatter). Structure:
            1. Frontmatter with title, description, publishedAt, author, category, tags
            2. Opening hook (1-2 paragraphs addressing the "why should I care")
            3. Well-structured content with ## headings
            4. Practical examples with ### subheadings
            5. Conclusion with key takeaways
            6. Call-to-action linking to relevant services

            Regional focus: Highlight differences between Washington (no state income tax) and Oregon
            (state income tax) when relevant to the topic."""),
            ("user", """Write an article on the following topic:

            Topic: {topic}

            {research_section}

            Additional Requirements:
            {requirements}

            Please write a complete article in MDX format with proper frontmatter.""")
        ])

    def write_article(
        self,
        topic: str,
        research_findings: Optional[str] = None,
        category: str = "Tax Planning",
        tags: Optional[list] = None,
        additional_requirements: str = ""
    ) -> str:
        """
        Write an article based on the topic and research findings.

        Args:
            topic: The main topic of the article
            research_findings: Research findings from the research agent
            category: Article category (default: "Tax Planning")
            tags: List of tags for the article
            additional_requirements: Any additional requirements or constraints

        Returns:
            Complete article in MDX format
        """
        print(f"✍️  Writing article on: {topic}")

        # Prepare research section
        research_section = ""
        if research_findings:
            research_section = f"""Research Findings:
{research_findings}

Use these research findings as the foundation for your article, but write in your own voice
and structure. Feel free to add additional context, examples, or insights based on your knowledge
of tax and accounting topics."""
        else:
            research_section = "No external research provided. Draw from your knowledge of accounting and tax topics."

        # Prepare tags
        if tags is None:
            tags = []

        tags_info = f"Suggested tags: {', '.join(tags)}" if tags else "Generate appropriate tags based on the content"

        # Add metadata requirements
        full_requirements = f"""Category: {category}
{tags_info}
Author: FoxGlove CPA
Published Date: {datetime.now().strftime('%Y-%m-%d')}

{additional_requirements}"""

        # Generate article
        chain = self.writing_prompt | self.llm

        result = chain.invoke({
            "topic": topic,
            "research_section": research_section,
            "requirements": full_requirements
        })

        print("✓ Article written successfully")

        return result.content

    def revise_article(self, article_content: str, revision_notes: str) -> str:
        """
        Revise an existing article based on feedback.

        Args:
            article_content: The current article content
            revision_notes: Notes on what to revise

        Returns:
            Revised article content
        """
        print(f"✏️  Revising article based on feedback")

        revision_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional editor for FoxGlove CPA. Revise the article
            according to the feedback while maintaining the professional but approachable tone.

            Keep the same MDX format with frontmatter."""),
            ("user", """Current Article:
{article}

Revision Notes:
{notes}

Please provide the revised article in complete MDX format.""")
        ])

        chain = revision_prompt | self.llm

        result = chain.invoke({
            "article": article_content,
            "notes": revision_notes
        })

        print("✓ Article revised successfully")

        return result.content
