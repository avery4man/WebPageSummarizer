# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import openai
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv('.env')

# Get Azure OpenAI details from environment variables
AZURE_OPENAI_KEY = os.environ.get('AZURE_OPENAI_KEY')
AZURE_OPENAI_BASE = os.environ.get('AZURE_OPENAI_BASE')
AZURE_OPENAI_TYPE = os.environ.get('AZURE_OPENAI_TYPE')
AZURE_OPENAI_VERSION = os.environ.get('AZURE_OPENAI_VERSION')
AZURE_OPENAI_DEPLOYMENT = os.environ.get('AZURE_OPENAI_DEPLOYMENT')

# Set OpenAI API details
openai.api_key = AZURE_OPENAI_KEY
openai.api_base = AZURE_OPENAI_BASE
openai.api_type = AZURE_OPENAI_TYPE
openai.api_version = AZURE_OPENAI_VERSION

# Function to calculate cost based on model and tokens used
def calculate_cost(model, tokens):
    model_costs = {
        'gpt-4': 0.06,
        'gpt-3.5': 0.002,
        'gpt-35-turbo-16k': 0.06,
        'gpt-35-turbo': 0.02
    }
    for model_name, cost in model_costs.items():
        if model_name in model:
            return tokens / 1000 * cost
    return 0  # Unknown model

# Function to fetch a webpage
def fetch_webpage(url):
    return requests.get(url)

# Function to parse a webpage
def parse_webpage(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

# Function to generate a summary
def generate_summary(text):
    response = openai.ChatCompletion.create(
      engine=AZURE_OPENAI_DEPLOYMENT,
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize the following text: " + text}
        ]
    )
    summary = response['choices'][0]['message']['content'].strip()
    tokens = response['usage']['total_tokens']
    model = response['model']
    return summary, tokens, model

# Function to summarize a webpage
def summarize(url):
    response = fetch_webpage(url)
    text = parse_webpage(response)
    summary, tokens, model = generate_summary(text)
    cost = calculate_cost(model, tokens)
    return summary, tokens, cost, model

# Main function of the app
if __name__ == "__main__":
    # Ask user for a URL
    url = input("Enter a URL: ")
    # Summarize the webpage at the given URL
    summary, tokens, cost, model = summarize(url)
    # Print the summary, tokens used, cost, and models
    print(f'Summary: {summary}\nTokens used: {tokens}\nCost: ${cost:.2f}\nModel: {model}')
