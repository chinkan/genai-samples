# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a collection of Jupyter notebooks demonstrating various Generative AI use cases, organized into categories for preprocessing, AI agents, and workflows.

## Development Environment Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # Linux/Mac: source .venv/bin/activate
   ```

2. Install dependencies - Note that different notebooks may have specific requirements:
   - General dependencies: `pip install -r requirements.txt` (if available in notebook directories)
   - Workflow examples: `pip install -r notebooks/4-workflows/requirements.txt`

3. Environment configuration:
   - Copy `.env.sample` to `.env` and configure required API keys
   - Required services: Azure OpenAI, OpenAI, Azure AI Search, SharePoint, SerpAPI
   - See `.env.sample` for complete list of environment variables

## Key Technologies and Frameworks

### AI Agent Frameworks
- **LangChain**: Primary framework for building AI agents with tool integration
- **LangGraph**: Used for building stateful, multi-actor applications with ReAct patterns
- **AutoGen**: Microsoft's multi-agent conversation framework
- **Qwen Agent**: Code interpreter and fact-checking capabilities
- **Browser-Use**: AI-controlled browser automation for web scraping

### Web Scraping and Data Processing
- **Crawl4AI**: AI-powered web crawling with LLM capabilities
- **MarkItDown**: Document format conversion to markdown
- **SharePoint API**: Integration for enterprise document access

### Workflow Management
- **NetworkX**: Graph-based workflow representation
- **Custom GraphNode system**: For managing LangGraph processor dependencies

## Common Development Patterns

### Notebook Structure
All example notebooks follow a consistent pattern:
1. Package installation with `%pip install`
2. Environment variable loading with `dotenv`
3. LLM client initialization (Azure OpenAI preferred)
4. Tool/agent setup and execution
5. Streaming output demonstration

### LLM Client Configuration
The repository standardizes on Azure OpenAI:
```python
from langchain_openai import AzureChatOpenAI
llm = AzureChatOpenAI(
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
)
```

### Agent Implementation Patterns
- **Tool-calling agents**: Using `create_tool_calling_agent` with custom tools
- **ReAct agents**: Using `create_react_agent` for reasoning and acting
- **Memory management**: Using `MemorySaver` for conversation persistence
- **Streaming output**: Consistent use of streaming for real-time responses

### Azure AI Search Integration
When working with search functionality:
- Use `SearchIndexClient` for index management
- Implement custom `@tool` decorators for search operations
- Handle search results with proper filtering and ranking
- Support both simple and semantic query types

## Running Notebooks

Each notebook is self-contained and can be executed independently. Ensure proper environment setup before running:

1. Start Jupyter: `jupyter notebook` or use VS Code
2. Navigate to desired notebook category
3. Execute cells sequentially
4. Monitor for any missing dependencies and install as needed

## Browser Automation

For browser-use examples:
- Playwright installation required: `playwright install`
- Notebooks will open browser windows during execution
- Generated GIFs and screenshots saved to data/screenshots/
- Handle popup advertisements and loading states gracefully

## Troubleshooting

- **Missing API keys**: Check `.env` file configuration
- **Package conflicts**: Use fresh virtual environment
- **Browser automation issues**: Ensure Playwright browsers are installed
- **Azure services**: Verify service endpoints and API key permissions