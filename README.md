# Article Generation Workflow

An AI-powered workflow for generating professional, approachable articles for the FoxGlove CPA blog using LangGraph, LangChain, and OpenAI.

## Overview

This workflow uses a multi-agent system to research topics and write high-quality articles:

- **Research Agent**: Gathers information from web sources or uses LLM knowledge
- **Writing Agent**: Creates professional, approachable content matching your brand voice
- **LangGraph Workflow**: Orchestrates the agents through research → writing → saving phases

## Features

- **Professional but Approachable Tone**: Matches your existing article style
-  **Optional Web Research**: Drop in a URL to research specific sources
-  **Customizable**: Set category, tags, and additional requirements
-  **MDX Output**: Generates properly formatted articles with frontmatter
-  **CLI Interface**: Easy command-line usage

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Verify Installation

```bash
python generate_article.py --help
```

## Usage

### Basic Usage

Generate an article from a topic:

```bash
python generate_article.py --topic "Quarterly Tax Planning Tips"
```

### With Research URL

Research a specific article and generate content:

```bash
python generate_article.py \
  --topic "Home Office Deduction for Remote Workers" \
  --url "https://www.irs.gov/businesses/small-businesses-self-employed/home-office-deduction"
```

### With Custom Settings

Specify category, tags, and requirements:

```bash
python generate_article.py \
  --topic "S-Corp vs LLC: Which is Right for You?" \
  --category "Business Structure" \
  --tags "s-corp,llc,entity-selection,tax-planning" \
  --requirements "Focus on Washington and Oregon state-specific considerations. Include 2024 tax year thresholds."
```

### Custom Filename

Specify a custom filename:

```bash
python generate_article.py \
  --topic "Estimated Tax Payment Deadlines" \
  --filename "estimated-taxes-2024.mdx"
```

### Interactive Mode

Run in interactive mode with prompts:

```bash
python generate_article.py --interactive
```

## CLI Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--topic` | `-t` | The article topic | Yes |
| `--url` | `-u` | URL to research (optional) | No |
| `--category` | `-c` | Article category (default: "Tax Planning") | No |
| `--tags` | | Comma-separated tags | No |
| `--requirements` | `-r` | Additional requirements | No |
| `--filename` | `-f` | Custom output filename | No |
| `--interactive` | `-i` | Interactive mode | No |

## Workflow Architecture

### Agents

#### Research Agent
- **Model**: GPT-4o-mini (fast and cost-effective)
- **Functions**:
  - `research_from_url()`: Scrapes and analyzes web articles
  - `research_from_topic()`: Uses LLM knowledge for research
- **Output**: Structured research findings with key insights

#### Writing Agent
- **Model**: GPT-4o (high quality)
- **Functions**:
  - `write_article()`: Generates complete articles
  - `revise_article()`: Revises based on feedback
- **Style**: Professional but approachable, example-driven

### LangGraph Workflow

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  RESEARCH   │  ← Gather information from URL or topic
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   WRITE     │  ← Generate article with research findings
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    SAVE     │  ← Save to content/articles/
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     END     │
└─────────────┘
```

## Project Structure

```
LucasSite/
├── workflows/
│   ├── agents/
│   │   ├── research_agent.py    # Research agent
│   │   └── writing_agent.py     # Writing agent
│   ├── utils/
│   │   └── web_scraper.py       # Web scraping utility
│   └── article_workflow.py      # LangGraph workflow
├── content/
│   └── articles/                # Generated articles saved here
├── generate_article.py          # CLI entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── ARTICLE_WORKFLOW.md          # This file
```

## Examples

### Example 1: Tax Planning Article

```bash
python generate_article.py \
  --topic "Tax Loss Harvesting Strategies for 2024" \
  --category "Tax Planning" \
  --tags "tax-loss-harvesting,investment,tax-strategy" \
  --requirements "Include specific examples with dollar amounts. Focus on small business owners and professionals."
```

### Example 2: Research-Based Article

```bash
python generate_article.py \
  --topic "New IRS Guidance on Employee Retention Credit" \
  --url "https://www.irs.gov/newsroom/employee-retention-credit" \
  --category "Tax Updates" \
  --tags "erc,tax-credits,covid-relief"
```

### Example 3: Regional Focus

```bash
python generate_article.py \
  --topic "State Tax Differences: Washington vs Oregon for Small Businesses" \
  --category "Tax Planning" \
  --tags "washington,oregon,state-tax,small-business" \
  --requirements "Highlight specific scenarios where WA no-income-tax advantage is significant vs OR deductions"
```

## Article Style Guide

The writing agent is configured to match your existing article style:

- **Opening Hook**: Starts with a common question or pain point
- **Clear Structure**: Uses ## and ### headings effectively
- **Practical Examples**: Includes real dollar amounts and scenarios
- **Professional but Approachable**: Uses "you" and "we", conversational tone
- **Actionable**: Focus on what readers should do, not just theory
- **Regional Focus**: Highlights WA/OR differences when relevant
- **Strong CTA**: Ends with clear next steps and service links

## Customization

### Modify Agent Behavior

Edit the system prompts in:
- [research_agent.py](workflows/agents/research_agent.py) - Research style and focus
- [writing_agent.py](workflows/agents/writing_agent.py) - Writing style and tone

### Change Models

Update model names in agent constructors:
- Research Agent: Default `gpt-4o-mini` (fast, cheap)
- Writing Agent: Default `gpt-4o` (high quality)

### Adjust Workflow

Modify [article_workflow.py](workflows/article_workflow.py) to:
- Add review/editing steps
- Include fact-checking node
- Add multi-round revision loops

## Troubleshooting

### "OPENAI_API_KEY not found"

Make sure you've:
1. Created a `.env` file from `.env.example`
2. Added your OpenAI API key to `.env`
3. Not committed `.env` to git (it should be in .gitignore)

### "Research failed" or URL scraping issues

- Some websites block scrapers - try a different source
- The workflow will fall back to topic research if URL fails
- Check that the URL is publicly accessible

### "Import errors" or module not found

Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### Articles not matching expected style

- Review generated articles and note patterns
- Adjust the system prompt in `writing_agent.py`
- Provide more specific requirements via `--requirements`

## Cost Estimation

Approximate costs per article (using OpenAI pricing):

- **Research**: ~$0.01-0.05 (GPT-4o-mini)
- **Writing**: ~$0.10-0.30 (GPT-4o)
- **Total**: ~$0.15-0.35 per article

Costs vary based on:
- Article length and complexity
- Amount of research material
- Number of revisions

## Roadmap

Future enhancements:

- [ ] Add revision loop with feedback
- [ ] SEO optimization suggestions
- [ ] Multi-article series planning
- [ ] Integration with CMS/publishing workflow
- [ ] Fact-checking and source citation
- [ ] Image generation integration
- [ ] Analytics and performance tracking

## Support

For issues or questions:
1. Check this documentation
2. Review example articles in `content/articles/`
3. Inspect workflow logs for error details

---

**Generated articles are starting points** - always review and edit to ensure accuracy, compliance, and alignment with your brand voice!
