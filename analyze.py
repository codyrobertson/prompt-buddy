import json
import os
from langchain_client import LangchainClient
from openai_client import OpenAIClient
from pinecone_client import PineconeClient

class PromptAnalyzer:
    def __init__(self, pinecone_api_key, openai_api_key, pinecone_index_name, google_api_key, google_cse_id):
        self.pinecone_client = PineconeClient(api_key=pinecone_api_key)
        self.openai_client = OpenAIClient(api_key=openai_api_key)
        self.pinecone_index_name = pinecone_index_name
        self.google_api_key = google_api_key
        self.google_cse_id = google_cse_id

    def analyze(self, prompt):
        # Call the OpenAI API to generate a text completion
        completion = self.openai_client.generate_text(prompt)

        # Extract the last sentence of the completion
        last_sentence = completion.split(".")[-2].strip() + "."

        # Call the LangChain API to translate the last sentence to Spanish
        langchain_client = LangchainClient()
        translation = langchain_client.translate_text(last_sentence, "en", "es")

        # Call the Pinecone API to search for similar prompts
        search_results = self.pinecone_client.search(self.pinecone_index_name, [translation], num_results=5)

        # Extract the prompts from the search results
        prompts = [result["document"]["text"] for result in search_results]

        # Combine the original prompt, the completion, and the translated sentence into a single response
        response = {
            "prompt": prompt,
            "completion": completion,
            "translation": translation,
            "prompts": prompts
        }

        return json.dumps(response)
