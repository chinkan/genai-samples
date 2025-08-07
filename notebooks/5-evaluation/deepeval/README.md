# LLM Evaluation with DeepEval

This folder contains examples of evaluating LLM agents using the DeepEval framework.

## Contents

- `react-agent-evaluation.ipynb` - Complete evaluation notebook for the React agent from langchain-agent example
- `evaluation_questions.csv` - Sample evaluation questions with expected answers and citations
- `README.md` - This documentation file

## Overview

The evaluation notebook demonstrates how to:

1. **Setup Evaluation Environment**
   - Configure DeepEval metrics (Answer Relevancy, Faithfulness, Contextual Relevancy)
   - Initialize React agent with Azure AI Search integration
   - Load evaluation questions from CSV/Excel files

2. **Run Comprehensive Evaluation**
   - Query the React agent for each question
   - Extract answers and citations automatically
   - Apply multiple DeepEval metrics for quality assessment
   - Calculate overall scores and correctness ratings

3. **Generate Results and Analysis**
   - Export detailed results to CSV and Excel formats
   - Provide statistical analysis of evaluation metrics
   - Generate visualizations (optional with matplotlib)

## Key Features

### DeepEval Metrics Used
- **Answer Relevancy**: Measures how relevant the answer is to the question
- **Faithfulness**: Evaluates if the answer is grounded in the provided context
- **Contextual Relevancy**: Assesses the relevance of retrieved context
- **Citation Accuracy**: Custom metric to verify proper source attribution

### Output Format
The evaluation produces results in the requested Excel format with columns:
- `question` - The evaluation question
- `expected_answer` - The expected/reference answer
- `expected_citation` - The expected source citation
- `actual_answer` - The agent's actual response
- `actual_citation` - The citations provided by the agent
- `correctness` - Pass/Fail based on threshold scoring
- `answer_score` - Overall quality score (0-1)
- `no_of_citation_correct` - Number of correct citations found

## Usage

1. **Setup Environment**
   ```bash
   pip install deepeval langchain langchain-community langchain-openai langgraph azure-search-documents pandas openpyxl
   ```

2. **Configure Environment Variables**
   - Copy `.env.sample` to `.env`
   - Fill in your Azure OpenAI and Azure AI Search credentials

3. **Run Evaluation**
   - Open `react-agent-evaluation.ipynb` in Jupyter
   - Execute cells sequentially
   - Results will be saved to `react_agent_evaluation_results.csv` and `.xlsx`

## Customization

### Adding New Questions
Edit `evaluation_questions.csv` to add more evaluation scenarios:
```csv
question,expected_answer,expected_citation
"Your question here","Expected answer","Source.pdf"
```

### Modifying Metrics
The notebook supports adding custom DeepEval metrics:
```python
custom_metric = GEval(
    name="Custom Metric",
    criteria="Your evaluation criteria",
    evaluation_steps=["Step 1", "Step 2"],
    threshold=0.7
)
```

### Changing Evaluation Thresholds
Adjust the threshold values in metric initialization:
```python
answer_relevancy_metric = AnswerRelevancyMetric(
    threshold=0.8,  # Increase for stricter evaluation
    model="gpt-4"
)
```

## Integration with CI/CD

The evaluation can be automated as part of your development pipeline:

1. **Automated Testing**: Run evaluation on agent changes
2. **Performance Monitoring**: Track evaluation scores over time  
3. **Quality Gates**: Block deployments if scores drop below thresholds
4. **Regression Testing**: Ensure changes don't degrade performance

## Expected Results

The evaluation provides insights into:
- **Agent Accuracy**: How well the agent answers domain-specific questions
- **Source Attribution**: Whether the agent properly cites information sources
- **Context Usage**: How effectively the agent uses retrieved information
- **Consistency**: Variation in performance across different question types

## Troubleshooting

### Common Issues
1. **API Rate Limits**: Add delays between evaluations if hitting limits
2. **Missing Context**: Ensure Azure AI Search index is properly populated
3. **Metric Failures**: Check that DeepEval model (GPT-4) is accessible
4. **Memory Issues**: Process questions in smaller batches for large datasets

### Performance Tips
- Use smaller question batches for initial testing
- Cache search results to avoid repeated API calls
- Run evaluation during off-peak hours for better API performance
- Consider using local LLM models for evaluation to reduce costs