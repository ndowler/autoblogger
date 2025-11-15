"""LangGraph workflow for article generation."""
from typing import TypedDict, Optional, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
import operator
import sys
import os

# Add agents to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.research_agent import ResearchAgent
from agents.writing_agent import WritingAgent


class ArticleState(TypedDict):
    """State for the article generation workflow."""
    topic: str
    research_url: Optional[str]
    research_findings: Optional[str]
    category: str
    tags: list[str]
    additional_requirements: str
    article_content: str
    output_filename: str
    messages: Annotated[list, operator.add]
    error: Optional[str]


class ArticleWorkflow:
    """LangGraph workflow for generating articles with research and writing agents."""

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.writing_agent = WritingAgent()
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(ArticleState)

        # Add nodes
        workflow.add_node("research", self._research_node)
        workflow.add_node("write", self._write_node)
        workflow.add_node("save", self._save_node)

        # Define edges
        workflow.set_entry_point("research")
        workflow.add_edge("research", "write")
        workflow.add_edge("write", "save")
        workflow.add_edge("save", END)

        return workflow.compile()

    def _research_node(self, state: ArticleState) -> ArticleState:
        """Research node - gathers information from URL or topic."""
        print("\n" + "="*60)
        print("RESEARCH PHASE")
        print("="*60)

        try:
            if state.get("research_url"):
                # Research from URL
                findings = self.research_agent.research_from_url(
                    url=state["research_url"],
                    topic=state["topic"]
                )

                if findings:
                    state["research_findings"] = findings
                    state["messages"].append(
                        HumanMessage(content=f"Research completed from URL: {state['research_url']}")
                    )
                else:
                    # Fallback to topic research if URL fails
                    print("⚠️  URL research failed, falling back to topic research")
                    findings = self.research_agent.research_from_topic(
                        topic=state["topic"],
                        additional_context=state.get("additional_requirements", "")
                    )
                    state["research_findings"] = findings
                    state["messages"].append(
                        HumanMessage(content="URL research failed, used topic research instead")
                    )
            else:
                # Research from topic only
                findings = self.research_agent.research_from_topic(
                    topic=state["topic"],
                    additional_context=state.get("additional_requirements", "")
                )
                state["research_findings"] = findings
                state["messages"].append(
                    HumanMessage(content="Research completed from topic knowledge")
                )

            print(f"\n📊 Research findings preview:")
            print(state["research_findings"][:500] + "...\n")

        except Exception as e:
            error_msg = f"Research failed: {str(e)}"
            print(f"❌ {error_msg}")
            state["error"] = error_msg
            state["research_findings"] = None

        return state

    def _write_node(self, state: ArticleState) -> ArticleState:
        """Writing node - creates the article."""
        print("\n" + "="*60)
        print("WRITING PHASE")
        print("="*60)

        try:
            article_content = self.writing_agent.write_article(
                topic=state["topic"],
                research_findings=state.get("research_findings"),
                category=state.get("category", "Tax Planning"),
                tags=state.get("tags", []),
                additional_requirements=state.get("additional_requirements", "")
            )

            state["article_content"] = article_content
            state["messages"].append(
                HumanMessage(content="Article written successfully")
            )

            print(f"\n📝 Article preview:")
            print(article_content[:500] + "...\n")

        except Exception as e:
            error_msg = f"Writing failed: {str(e)}"
            print(f"❌ {error_msg}")
            state["error"] = error_msg

        return state

    def _save_node(self, state: ArticleState) -> ArticleState:
        """Save node - saves the article to file."""
        print("\n" + "="*60)
        print("SAVING PHASE")
        print("="*60)

        try:
            if state.get("error"):
                print(f"❌ Skipping save due to previous error: {state['error']}")
                return state

            # Determine output filename
            if not state.get("output_filename"):
                # Generate filename from topic
                filename = state["topic"].lower()
                filename = filename.replace(" ", "-")
                filename = "".join(c for c in filename if c.isalnum() or c == "-")
                filename = f"{filename}.mdx"
                state["output_filename"] = filename

            # Construct full path
            output_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "content",
                "articles",
                state["output_filename"]
            )

            # Save article
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(state["article_content"])

            print(f"✅ Article saved to: {output_path}")

            state["messages"].append(
                HumanMessage(content=f"Article saved to {output_path}")
            )

        except Exception as e:
            error_msg = f"Save failed: {str(e)}"
            print(f"❌ {error_msg}")
            state["error"] = error_msg

        return state

    def generate_article(
        self,
        topic: str,
        research_url: Optional[str] = None,
        category: str = "Tax Planning",
        tags: Optional[list] = None,
        additional_requirements: str = "",
        output_filename: Optional[str] = None
    ) -> dict:
        """
        Generate an article using the workflow.

        Args:
            topic: The topic for the article
            research_url: Optional URL to research
            category: Article category
            tags: List of tags
            additional_requirements: Any additional requirements
            output_filename: Custom output filename (optional)

        Returns:
            Final state dictionary
        """
        print("\n" + "="*60)
        print("ARTICLE GENERATION WORKFLOW")
        print("="*60)
        print(f"Topic: {topic}")
        if research_url:
            print(f"Research URL: {research_url}")
        print(f"Category: {category}")
        print(f"Tags: {tags or 'auto-generated'}")
        print("="*60)

        # Initialize state
        initial_state = {
            "topic": topic,
            "research_url": research_url,
            "research_findings": None,
            "category": category,
            "tags": tags or [],
            "additional_requirements": additional_requirements,
            "article_content": "",
            "output_filename": output_filename,
            "messages": [],
            "error": None
        }

        # Run workflow
        final_state = self.workflow.invoke(initial_state)

        # Print summary
        print("\n" + "="*60)
        print("WORKFLOW COMPLETE")
        print("="*60)

        if final_state.get("error"):
            print(f"❌ Completed with errors: {final_state['error']}")
        else:
            print("✅ Article generated successfully!")
            print(f"📁 Saved as: {final_state.get('output_filename')}")

        print("="*60 + "\n")

        return final_state


if __name__ == "__main__":
    # Example usage
    workflow = ArticleWorkflow()

    # Example 1: Generate article with research URL
    workflow.generate_article(
        topic="Home Office Deduction for Remote Workers",
        research_url="https://www.irs.gov/businesses/small-businesses-self-employed/home-office-deduction",
        category="Tax Deductions",
        tags=["home office", "deductions", "remote work"],
        additional_requirements="Focus on 2024 tax year rules and common mistakes"
    )
