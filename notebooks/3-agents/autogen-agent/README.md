# AutoGen Deep Search Agents with ScrapingDog API & OpenRouter

This directory contains a comprehensive implementation of a multi-agent research system using AutoGen v0.4, ScrapingDog API, and OpenRouter for deep web research capabilities with multiple AI models.

## Overview

The `autogen-deep-search-agents.ipynb` notebook demonstrates a sophisticated multi-agent system that collaborates to perform comprehensive web research. The system consists of four specialized agents, each powered by different AI models through OpenRouter, working together to deliver high-quality, well-cited research reports.

## Architecture

### Agent Roles & AI Models

1. **Planning Agent** 🎯 **(Llama 3.1 70B Instruct)**
   - Analyzes research queries and breaks them into actionable tasks
   - Creates structured research plans with clear priorities
   - Identifies authoritative sources and search strategies
   - Ensures comprehensive coverage of research topics
   - **Why Llama 3.1 70B**: Excellent for logical planning and structured task breakdown

2. **Web Search Agent** 🔍 **(Google Gemini Pro 1.5)**
   - Executes web scraping using ScrapingDog API
   - Extracts relevant information from web sources
   - Evaluates source credibility and data quality
   - Provides structured findings and summaries
   - **Why Gemini Pro 1.5**: Superior web content analysis and information extraction

3. **Citation Agent** 📚 **(Claude 3.5 Sonnet)**
   - Validates source credibility and authority
   - Creates properly formatted citations (APA style)
   - Identifies potential bias or limitations in sources
   - Ensures all claims are properly attributed
   - **Why Claude 3.5 Sonnet**: Exceptional academic writing and citation formatting

4. **Finalize Agent** 📝 **(Claude 4 Sonnet)**
   - Synthesizes information from all research phases using advanced reasoning
   - Compiles comprehensive, well-structured reports with deep insights
   - Identifies gaps and recommendations with strategic analysis
   - Provides clear conclusions and actionable insights with risk assessment
   - **Why Claude 4 Sonnet**: State-of-the-art reasoning and synthesis capabilities

### Technology Stack

- **AutoGen v0.4**: Multi-agent framework with asynchronous messaging
- **OpenRouter**: Multi-model API access for diverse AI capabilities
- **ScrapingDog API**: Web scraping with JavaScript rendering support
- **Multiple AI Models**: 
  - Llama 3.1 70B Instruct (Meta)
  - Gemini Pro 1.5 (Google)
  - Claude 3.5 & 4 Sonnet (Anthropic)
- **BeautifulSoup4**: HTML parsing and content extraction
- **Python-dotenv**: Environment variable management

## Key Features

### 🚀 Advanced Web Scraping
- **JavaScript Rendering**: Handles dynamic content and SPAs
- **Geo-targeting**: Supports location-based content scraping
- **Error Handling**: Robust retry logic and failure recovery
- **Content Processing**: Automatic text extraction and cleaning

### 🤖 Intelligent Agent Collaboration with Multi-Model AI
- **Asynchronous Communication**: Efficient message passing between agents
- **Specialized Models**: Each agent uses the optimal AI model for its task
- **Model Diversity**: Leverages strengths of different AI providers (Meta, Google, Anthropic)
- **Quality Control**: Multiple validation layers with model-specific expertise
- **Adaptive Planning**: Dynamic research strategies based on findings

### 📊 Research Quality Assurance
- **Source Validation**: Credibility assessment and authority verification
- **Academic Citations**: Proper APA format citation generation
- **Cross-referencing**: Information verification across multiple sources
- **Comprehensive Reports**: Structured final deliverables

### 🎛️ Customization Options
- **Configurable Models**: Easy switching between different AI models via OpenRouter
- **Agent Specialization**: Adjustable system messages and behaviors per agent
- **Research Depth**: Controllable investigation thoroughness
- **Interactive Mode**: Real-time research query processing
- **Cost Optimization**: Model selection based on complexity and budget
- **Extensible Tools**: Easy integration of additional data sources

## Prerequisites

### Required Services
1. **ScrapingDog API Account**
   - Sign up at: https://www.scrapingdog.com/
   - Get API key from dashboard
   - Free tier: 1000 requests/month

2. **OpenRouter API Account**
   - Sign up at: https://openrouter.ai/
   - Get API key from dashboard
   - Access to multiple AI models including Claude 4 Sonnet
   - Pay-per-use pricing model

### Environment Setup

1. **Clone and Navigate**
   ```bash
   cd notebooks/3-agents/autogen-agent/
   ```

2. **Install Dependencies**
   ```bash
   pip install -U \"autogen-agentchat\" \"autogen-ext[openai]\" requests beautifulsoup4 python-dotenv
   ```

3. **Configure Environment Variables**
   
   Copy the required variables to your `.env` file:
   ```env
   # ScrapingDog API
   SCRAPINGDOG_API_KEY=your_scrapingdog_api_key_here
   
   # OpenRouter Configuration
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```

## Usage Examples

### Basic Research Session
```python
# Simple research query
research_query = \"Latest developments in quantum computing and their impact on cybersecurity\"
await run_deep_search(research_query, max_rounds=10)
```

### Interactive Research Mode
```python
# Start interactive session
interactive_research()
# Enter queries when prompted
```

### Custom Model Configuration
```python
# Modify models for different agents
MODEL_CONFIGS = {
    \"planning\": \"meta-llama/llama-3.1-70b-instruct\",
    \"search\": \"google/gemini-pro-1.5\", 
    \"citation\": \"anthropic/claude-3.5-sonnet\",
    \"finalize\": \"anthropic/claude-3-5-sonnet-20241022\"  # Claude 4 Sonnet
}

# Create custom client
custom_client = create_openrouter_client(\"anthropic/claude-3-5-sonnet-20241022\")
```

## Sample Research Topics

### Technology Research
- \"Impact of artificial intelligence on software development practices\"
- \"Blockchain adoption in supply chain management 2024-2025\"
- \"Edge computing vs cloud computing performance comparison\"

### Market Analysis
- \"Electric vehicle market trends and consumer adoption patterns\"
- \"Remote work technology solutions market growth\"
- \"Sustainable energy investment opportunities\"

### Academic Research
- \"Climate change mitigation strategies effectiveness analysis\"
- \"Digital education tools impact on student learning outcomes\"
- \"Healthcare AI applications regulatory landscape\"

## API Integration Details

### OpenRouter Multi-Model Access
- **Base URL**: `https://openrouter.ai/api/v1`
- **Model Selection**: Access to 100+ AI models from multiple providers
- **Pay-per-use**: Only pay for what you use, no monthly commitments
- **Model Routing**: Automatic failover and load balancing
- **Usage Tracking**: Detailed analytics per model and request

#### Model Selection Rationale
| Agent | Model | Provider | Strengths | Cost/1M tokens |
|-------|-------|----------|-----------|----------------|
| Planning | Llama 3.1 70B | Meta | Logical reasoning, structured output | ~$0.90 |
| Search | Gemini Pro 1.5 | Google | Web content analysis, large context | ~$3.50 |
| Citation | Claude 3.5 Sonnet | Anthropic | Academic writing, precision | ~$3.00 |
| Finalize | Claude 4 Sonnet | Anthropic | Advanced reasoning, synthesis | ~$15.00 |

### ScrapingDog API Features
- **Base URL**: `https://api.scrapingdog.com/scrape`
- **JavaScript Rendering**: Dynamic content support
- **Geo-targeting**: Country-specific content access
- **Rate Limits**: Varies by subscription plan
- **Response Format**: Raw HTML with metadata

### Error Handling
- **HTTP Status Codes**: 200 (success), 410 (timeout), 404 (invalid URL), 403 (limit reached)
- **Retry Logic**: Automatic retries for transient failures
- **Content Validation**: Checks for successful content extraction
- **Fallback Strategies**: Alternative approaches for failed requests

## Output Format

### Research Reports Include:
1. **Executive Summary**: Key findings overview
2. **Detailed Analysis**: In-depth investigation results
3. **Source Citations**: APA-formatted references
4. **Credibility Assessment**: Source reliability evaluation
5. **Conclusions**: Actionable insights and recommendations
6. **Research Gaps**: Areas requiring additional investigation

### Citation Format (APA Style)
```
Author, A. A. (Year, Month Date). Title of web page. Website Name. URL
```

## Performance Optimization

### Efficiency Tips
- **Batch Processing**: Group similar URLs for efficient scraping
- **Content Filtering**: Focus on relevant sections to reduce processing time
- **Caching**: Store frequently accessed content locally
- **Rate Limiting**: Respect API limits to avoid throttling

### Cost Management
- **Request Optimization**: Minimize unnecessary API calls
- **Content Limits**: Truncate lengthy content for processing efficiency
- **Error Prevention**: Validate URLs before scraping
- **Plan Selection**: Choose appropriate ScrapingDog subscription tier

## Troubleshooting

### Common Issues

1. **OpenRouter Model Configuration Error**
   ```
   Error: ValueError: model_info is required when model name is not a valid OpenAI model
   Solution: The notebook now includes proper ModelInfo configuration for OpenRouter models
   ```

2. **API Key Errors**
   ```
   Error: Invalid API key
   Solution: Verify OPENROUTER_API_KEY and SCRAPINGDOG_API_KEY in .env file
   ```

3. **Rate Limit Exceeded**
   ```
   Error: HTTP 403 - Request limit reached
   Solution: Check OpenRouter credits or upgrade plan
   ```

4. **Model Access Issues**
   ```
   Error: Model not available
   Solution: Verify model names in OpenRouter dashboard and check account permissions
   ```

5. **Scraping Failures**
   ```
   Error: HTTP 410 - Request timeout
   Solution: Retry with shorter timeout or different URL
   ```

6. **Agent Communication Issues**
   ```
   Error: Agent not responding
   Solution: Check OpenRouter service status and API quotas
   ```

### Debug Mode
Enable detailed logging by adding:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Extension Opportunities

### Additional Features
- **PDF Document Processing**: Integrate document analysis capabilities
- **Image Content Extraction**: Add OCR for image-based content
- **Social Media Integration**: Include social platform data sources
- **Real-time Monitoring**: Set up continuous research updates
- **Collaborative Workspaces**: Multi-user research sessions

### Custom Tools
- **Database Integration**: Store and retrieve research history
- **Export Formats**: Generate reports in PDF, Word, or PowerPoint
- **Visualization**: Create charts and graphs from research data
- **API Webhooks**: Trigger research based on external events

## Security Considerations

### Data Privacy
- **API Key Management**: Store keys securely, never commit to version control
- **Request Logging**: Avoid logging sensitive query parameters
- **Content Sanitization**: Clean scraped content to remove malicious scripts
- **Access Controls**: Implement proper authentication for multi-user deployments

### Compliance
- **Rate Limiting**: Respect website terms of service and robot.txt
- **Data Retention**: Implement appropriate data lifecycle policies
- **User Consent**: Ensure proper permissions for data collection
- **Regional Regulations**: Comply with GDPR, CCPA, and other privacy laws

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-capability`
3. Implement changes with tests
4. Submit pull request with detailed description

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for function parameters
- Include docstrings for all public methods
- Write unit tests for new functionality

## License

This project is part of the genai-samples repository. Please refer to the main repository license for usage terms.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review AutoGen documentation: https://microsoft.github.io/autogen/
3. Visit ScrapingDog docs: https://docs.scrapingdog.com/
4. Create an issue in the main repository

## Changelog

### v1.0.0 (Current)
- Initial implementation with AutoGen v0.4
- ScrapingDog API integration
- Four-agent research system
- Interactive and batch research modes
- Comprehensive documentation and examples

---

*This implementation showcases the power of multi-agent systems for complex research tasks, combining the latest in agent frameworks with robust web scraping capabilities.*