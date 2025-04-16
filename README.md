# MiniMe - Dual-Purpose Interactive Marketing Assistant

MiniMe is a specialized chatbot that combines marketing task execution with educational components, helping users both accomplish marketing tasks and learn marketing concepts simultaneously.

## Features

- **Marketing Task Execution**
  - Brand Analysis
  - Value Proposition Formulation
  - Target Audience Identification
  - Creative Concept Generation & Copywriting
  - Task-Specific Function Calling

- **Educational Component**
  - Pre-Task Explanations
  - Process Walkthroughs
  - Post-Task Summaries
  - Contextual Learning Prompts

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: LangChain, OpenAI
- **Vector Database**: Pinecone
- **Version Control**: Git

## Project Structure

```
minime/
├── app/                    # Streamlit application
│   ├── pages/             # Streamlit pages
│   ├── components/        # Reusable UI components
│   └── utils/             # Utility functions
├── backend/               # Core application logic
│   ├── rag/              # RAG implementation
│   ├── functions/        # Marketing task functions
│   └── models/           # Data models
├── data/                  # Data and knowledge base
│   ├── raw/              # Raw marketing content
│   └── processed/        # Processed and vectorized content
├── tests/                 # Test suite
├── config/                # Configuration files
└── docs/                  # Documentation
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/minime.git
   cd minime
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Run the application:
   ```bash
   streamlit run app/main.py
   ```

## Development Workflow

This project follows a sprint-based development approach with dedicated branches for each milestone:

1. `main` - Production-ready code
2. `sprint-ui-prototype` - UI development
3. `sprint-rag-integration` - RAG implementation
4. `sprint-function-calling` - Marketing task functions
5. `sprint-educational-integration` - Educational content
6. `sprint-backend-robustness` - Backend improvements
7. `sprint-final-integration` - Final integration

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

MIT License 