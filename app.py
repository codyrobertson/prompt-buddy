from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import os
from analyze import PromptAnalyzer
from suggestion import PromptOptimizer

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    message = request.form.get('message', '').strip()

    # Process the message and call the appropriate AI functions
    if message.lower().startswith("analyze"):
        prompt = message[7:].strip()
        response = prompt_analyzer.analyze(prompt)
        return jsonify(type="analysis", data=response)

    elif message.lower().startswith("suggest"):
        prompt = message[7:].strip()
        response = prompt_optimizer.suggest(prompt)
        return jsonify(type="suggestion", data=response)

    elif message.lower().startswith("browser"):
        prompt = message[7:].strip()
        additional_info = fetch_information(prompt, prompt_analyzer.openai_client)
        if additional_info:
            # Extract the title, snippet, and link from the additional_info string
            # You may need to modify the fetch_information function to return these values separately
            return jsonify(type="browser", data={"title": title, "snippet": snippet, "link": link})
        else:
            return jsonify(type="message", data="I couldn't find any relevant information.")

    # If no command is recognized, return a default message
    return jsonify(type="message", data="I didn't understand your command. Please try again.")

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Run the Flask app
    app.run(debug=True)

if __name__ == '__main__':
    main()
