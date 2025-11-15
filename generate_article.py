#!/usr/bin/env python3
"""
CLI tool for generating articles using the LangGraph workflow.

Usage:
    python generate_article.py --topic "Your Article Topic" [options]

Examples:
    # Generate article with just a topic
    python generate_article.py --topic "Quarterly Tax Deadlines 2024"

    # Generate article with research from URL
    python generate_article.py --topic "Home Office Deduction" --url "https://www.irs.gov/..."

    # Generate article with custom category and tags
    python generate_article.py --topic "LLC vs S-Corp" --category "Business Structure" --tags "llc,s-corp,entity-selection"

    # Generate article with additional requirements
    python generate_article.py --topic "Retirement Plans" --requirements "Focus on small businesses under 10 employees"
"""
import argparse
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add workflows to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'workflows'))
from article_workflow import ArticleWorkflow


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate articles using AI-powered research and writing agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate article from topic only:
    python generate_article.py --topic "Quarterly Tax Planning Tips"

  Generate article with research URL:
    python generate_article.py --topic "Home Office Deduction" \\
        --url "https://www.irs.gov/businesses/small-businesses-self-employed/home-office-deduction"

  Generate article with custom settings:
    python generate_article.py --topic "S-Corp Election Deadline" \\
        --category "Tax Planning" \\
        --tags "s-corp,deadlines,entity-selection" \\
        --requirements "Focus on 2024 tax year and include late election relief"

  Specify custom filename:
    python generate_article.py --topic "Estimated Tax Payments" \\
        --filename "estimated-taxes-guide.mdx"
        """
    )

    parser.add_argument(
        "--topic",
        "-t",
        required=True,
        help="The topic for the article (required)"
    )

    parser.add_argument(
        "--url",
        "-u",
        help="Optional URL to research for article content"
    )

    parser.add_argument(
        "--category",
        "-c",
        default="Tax Planning",
        help="Article category (default: Tax Planning)"
    )

    parser.add_argument(
        "--tags",
        help="Comma-separated list of tags (e.g., 's-corp,tax-planning,deductions')"
    )

    parser.add_argument(
        "--requirements",
        "-r",
        default="",
        help="Additional requirements or constraints for the article"
    )

    parser.add_argument(
        "--filename",
        "-f",
        help="Custom output filename (e.g., 'my-article.mdx'). If not specified, generated from topic"
    )

    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode with prompts for each field"
    )

    return parser.parse_args()


def interactive_mode():
    """Run the CLI in interactive mode."""
    print("\n" + "="*60)
    print("ARTICLE GENERATOR - Interactive Mode")
    print("="*60 + "\n")

    topic = input("Article Topic (required): ").strip()
    if not topic:
        print("❌ Topic is required!")
        sys.exit(1)

    url = input("Research URL (optional, press Enter to skip): ").strip() or None

    category = input("Category (default: Tax Planning): ").strip() or "Tax Planning"

    tags_input = input("Tags (comma-separated, optional): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

    requirements = input("Additional requirements (optional): ").strip() or ""

    filename = input("Custom filename (optional, press Enter to auto-generate): ").strip() or None

    return {
        "topic": topic,
        "research_url": url,
        "category": category,
        "tags": tags,
        "additional_requirements": requirements,
        "output_filename": filename
    }


def main():
    """Main entry point for the CLI."""
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("\nPlease set your OpenAI API key:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI API key to .env")
        print("  3. Run this script again")
        sys.exit(1)

    args = parse_args()

    # Get parameters
    if args.interactive:
        params = interactive_mode()
    else:
        # Parse tags
        tags = []
        if args.tags:
            tags = [tag.strip() for tag in args.tags.split(",")]

        params = {
            "topic": args.topic,
            "research_url": args.url,
            "category": args.category,
            "tags": tags,
            "additional_requirements": args.requirements,
            "output_filename": args.filename
        }

    # Initialize workflow
    print("\n🚀 Initializing Article Generation Workflow...\n")
    workflow = ArticleWorkflow()

    # Generate article
    try:
        final_state = workflow.generate_article(**params)

        if final_state.get("error"):
            print(f"\n❌ Article generation failed: {final_state['error']}")
            sys.exit(1)
        else:
            print("\n✅ Success! Your article has been generated.")
            print(f"\n📁 Location: content/articles/{final_state['output_filename']}")
            print("\nNext steps:")
            print("  1. Review the generated article")
            print("  2. Make any necessary edits")
            print("  3. Commit to your repository")
            print("  4. Deploy to see it live!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Article generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
