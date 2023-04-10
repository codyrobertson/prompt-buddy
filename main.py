import argparse
import os
import json
from dotenv import load_dotenv
from web_browser import validate_url, open_virtual_browser
from analyze import PromptAnalyzer
from suggestion import PromptOptimizer
from googleapiclient.discovery import build

def should_open_browser(prompt, openai_client):
    response = openai_client.generate(prompt)
    text = response.get('text', '').lower()
    return 'more information needed' in text

def fetch_information(prompt, openai_client):
    if should_open_browser(prompt, openai_client):
        search_results = search_web(prompt)
        if search_results:
            top_result = search_results[0]
            title = top_result.get('title', '')
            snippet = top_result.get('snippet', '')
            return f"Here's what I found:\nTitle: {title}\nSnippet: {snippet}"
        else:
            return "I couldn't find any relevant information."
    return ""

def search_web(query):
    results = google_client.cse().list(q=query, cx=GOOGLE_CSE_ID).execute()
    return results.get("items", [])

def handle_args(args, prompt_analyzer, prompt_optimizer):
    if args.help:
        parser.print_help()

    elif args.debug:
        print("Debugging mode activated.")

    elif args.analyze:
        prompt = input("Enter the prompt to analyze: ")
        analysis_result = prompt_analyzer.analyze_prompt(prompt)
        print("Analysis results:")
        print(json.dumps(analysis_result))

        additional_info = fetch_information(prompt, prompt_analyzer.openai_client)
        if additional_info:
            print("Additional information:")
            print(additional_info)

    elif args.suggest:
        prompt = input("Enter the prompt to suggest improvements: ")
        suggestion_result = prompt_optimizer.suggest_prompt(prompt)
        print("Suggested improvements:")
        print(json.dumps(suggestion_result))

    elif args.tokens:
        prompt = input("Enter the prompt to count tokens: ")
        count = len(prompt.split())
        print(f"There are {count} tokens in the prompt.")

    elif args.browser:
        url = input("Please enter a website URL: ")
        while not validate_url(url):
            print("Invalid URL. Please enter a valid website URL.")
            url = input("Please enter a website URL: ")
        open_virtual_browser(url)

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Set up PromptAnalyzer
    prompt_analyzer = PromptAnalyzer(
        pinecone_api_key=os.getenv("PINECONE_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        pinecone_index_name=os.getenv("PINECONE_INDEX_NAME"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        google_cse_id=os.getenv("GOOGLE_CSE_ID")
    )

    # Set up PromptOptimizer
    prompt_optimizer = PromptOptimizer()

    # Initialize the Google client
    google_client = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY"))
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Optimize your prompts using Langchain, Pinecone, and OpenAI.")
    parser.add_argument('--analyze', action='store_true', help='Analyze a given prompt')
    parser.add_argument('--suggest', action='store_true', help='Suggest improvements for a given prompt')
    parser.add_argument('--debug', action='store_true', help='Activate debugging mode')
    parser.add_argument('--tokens', action='store_true', help='Count the tokens in a given prompt')
    parser.add_argument('--browser', action='store_true', help='Open a webpage in a virtual browser')
    parser.add_argument('--help', action='store_true', help='Show this help message')

    args = parser.parse_args()

    # Handle the arguments
    handle_args(args, prompt_analyzer, prompt_optimizer)

if __name__ == '__main__':
    main()