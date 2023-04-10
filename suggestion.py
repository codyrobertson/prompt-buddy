import os
from dotenv import load_dotenv
from langchain_client import LangchainClient
from pinecone_client import PineconeClient
from openai_client import OpenAIClient

load_dotenv()

class PromptOptimizer:
    def __init__(self):
        self.langchain_client = LangchainClient(api_key=os.getenv("LANGCHAIN_API_KEY"))
        self.pinecone_client = PineconeClient(api_key=os.getenv("PINECONE_API_KEY"), index_name=os.getenv("PINECONE_INDEX_NAME"))
        self.openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))

    def suggest_prompt(self, prompt):
        # Get language chain suggestions
        langchain_response = self.langchain_client.optimize_prompt(prompt)
        langchain_suggestion = langchain_response.get('suggestion', prompt)

        # Get Pinecone suggestions
        pinecone_response = self.pinecone_client.suggest(prompt)
        pinecone_suggestion = pinecone_response.get('suggestion', prompt)

        # Get OpenAI suggestions
        openai_response = self.openai_client.generate(prompt)
        openai_suggestion = openai_response.get('text', prompt)

        # Return the suggested prompt
        return {
            'original_prompt': prompt,
            'langchain_suggestion': langchain_suggestion,
            'pinecone_suggestion': pinecone_suggestion,
            'openai_suggestion': openai_suggestion
        }