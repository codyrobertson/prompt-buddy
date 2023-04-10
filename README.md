# Prompt Optimization Tool

This Prompt Optimization Tool is a Flask-based web application that helps you analyze and optimize your prompts using Langchain, Pinecone, and OpenAI. It also provides additional information from the web using the Google Custom Search API.

## Features

- Analyze prompts using Langchain, Pinecone, and OpenAI
- Suggest improvements for prompts
- Count tokens in a given prompt
- Fetch additional information from the web using the Google Custom Search API
- Interactive web interface for easy usage

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/prompt-optimization-tool.git
cd prompt-optimization-tool
```

2. Install the required packages:

```
pip install -r requirements.txt
```

3. Set up your environment variables in a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
```

## Usage

Run the Flask application:

```
python app.py
```

Open your web browser and navigate to `http://127.0.0.1:5000/`. You should see the chat interface. Interact with the application by sending various commands like "analyze", "suggest", "tokens", and "browser".

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
