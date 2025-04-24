# Marketing Assistant API

A FastAPI-based backend service for a marketing assistant application that helps with various marketing tasks.

## Features

- Chat-based interface for marketing tasks
- Task-specific prompts and guidance
- Conversation history management
- Support for multiple marketing tasks:
  - Content Calendar Creation
  - Email Campaign Design
  - Social Media Ad Creation
  - Competitor Analysis

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `GET /`: Welcome message
- `POST /chat`: Send a message and get a response
- `GET /tasks`: List all available marketing tasks
- `GET /tasks/{task_id}`: Get details of a specific task

## Development

The project structure is organized as follows:

- `app/`: Main application package
  - `main.py`: FastAPI application setup
  - `backend.py`: Chat management and response generation
  - `handlers/`: Task-specific handlers
    - `task_handlers.py`: Marketing task definitions and prompts
  - `models/`: Data models
    - `chat.py`: Chat-related data models
    - `tasks.py`: Task-related data models
  - `routes/`: API routes
    - `chat.py`: Chat-related endpoints
    - `tasks.py`: Task-related endpoints

## License

MIT 