# GenAI Samples Collection

This repository contains a collection of Jupyter notebooks demonstrating various use cases of Generative AI technologies.

## Project Structure

```
genai-samples/
├── notebooks/                          # Main directory for all Jupyter notebooks
│   ├── 0-preprocessing/               # Data preprocessing examples
│   │   ├── markdown_conversion/       # Text to markdown conversion examples
│   │   ├── rag/                      # Retrieval Augmented Generation examples
│   │   └── web-scrapping/            # Web scraping examples
│   └── 3-agents/                     # AI Agent examples
│       └── qwen-agent/               # Qwen Agent examples with code interpreter
├── data/                             # Sample data for notebooks
│   └── raw/                          # Raw input data
└── .env.sample                       # Template for environment variables
```

## Setup and Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.sample` to `.env` and fill in your API keys

## Available Examples

### Preprocessing
- **Markdown Conversion**: Convert various document formats to markdown using LLMs
- **RAG (Retrieval Augmented Generation)**: Examples of implementing RAG systems
- **Web Scraping**: Web content extraction and analysis using LLMs
  - `browser-use.ipynb`: Demonstrates how to use Browser-Use agent to control browser programmatically for web interactions and data extraction
  - `crawl4ai-sample.ipynb`: Shows how to use crawl4ai for AI-powered web crawling and content extraction with LLM capabilities

### AI Agents
- **Qwen Agent**: Examples using Qwen's agent capabilities
  - `qwen-agent-example.ipynb`: Demonstrates using Qwen agent with code interpreter and Python executor for local LLM interactions

## Contributing

Feel free to contribute new examples or improve existing ones through pull requests.

## License

See the [LICENSE](LICENSE) file for details.
